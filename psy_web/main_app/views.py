from django.shortcuts import render, redirect
from .models import Question, Result, UserResponse, Option
from .forms import TestForm


def test_view(request):
    questions = Question.objects.filter(is_active=True)
    if not questions:
        return render(request, 'test.html', {'error': 'Нет активных вопросов'})

    if request.method == 'POST':
        form = TestForm(questions, request.POST)
        if form.is_valid():
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            # Очищаем старые ответы этого пользователя
            UserResponse.objects.filter(session_key=session_key).delete()

            total_score = 0
            for q in questions:
                field_name = f'question_{q.id}'
                raw_value = form.cleaned_data.get(field_name)
                if q.question_type == 'single':
                    option = Option.objects.get(id=raw_value)
                    UserResponse.objects.create(
                        session_key=session_key,
                        question=q,
                        option=option,
                        value=''
                    )
                    total_score += option.score
                elif q.question_type == 'multiple':
                    for opt_id in raw_value:
                        option = Option.objects.get(id=opt_id)
                        UserResponse.objects.create(
                            session_key=session_key,
                            question=q,
                            option=option,
                            value=''
                        )
                        total_score += option.score
                elif q.question_type == 'scale':
                    UserResponse.objects.create(
                        session_key=session_key,
                        question=q,
                        option=None,
                        value=str(raw_value)
                    )
                    total_score += int(raw_value)
                elif q.question_type == 'text':
                    UserResponse.objects.create(
                        session_key=session_key,
                        question=q,
                        option=None,
                        value=raw_value
                    )
                    text_lower = q.text.lower()
                    if 'имя' in text_lower:
                        request.session['first_name'] = raw_value
                    elif 'фамилия' in text_lower:
                        request.session['last_name'] = raw_value
                    elif 'возраст' in text_lower:
                        request.session['age'] = raw_value

            request.session['total_score'] = total_score
            return redirect('result')
    else:
        form = TestForm(questions)

    return render(request, 'test.html', {'form': form, 'questions': questions})


def result_view(request):
    total_score = request.session.get('total_score', 0)
    result = Result.objects.filter(
        min_score__lte=total_score,
        max_score__gte=total_score
    ).order_by('order').first()
    
    context = {
        'result': result,
        'total_score': total_score,
        'first_name': request.session.get('first_name', ''),
        'last_name': request.session.get('last_name', ''),
        'age': request.session.get('age', ''),
    }
    return render(request, 'result.html', context)