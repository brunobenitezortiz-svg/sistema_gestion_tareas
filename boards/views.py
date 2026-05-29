from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Board
from django.shortcuts import get_object_or_404
from .models import Board, TaskList, Card


@login_required
def home(request):
    boards = Board.objects.filter(owner=request.user)

    return render(request, 'boards/home.html', {
        'boards': boards
    })


@login_required
def create_board(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Board.objects.create(
            title=title,
            description=description,
            owner=request.user
        )

        return redirect('home')

    return render(request, 'boards/create_board.html')


@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    lists = board.lists.all()

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'lists': lists
    })


@login_required
def create_list(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')

        position = board.lists.count()

        TaskList.objects.create(
            title=title,
            board=board,
            position=position
        )

        return redirect('board_detail', board_id=board.id)

    return render(request, 'boards/create_list.html', {
        'board': board
    })

@login_required
def create_card(request, list_id):
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        position = task_list.cards.count()

        Card.objects.create(
            title=title,
            description=description,
            task_list=task_list,
            position=position
        )

        return redirect('board_detail', board_id=task_list.board.id)

    return render(request, 'boards/create_card.html', {
        'task_list': task_list
    })

@login_required
def edit_card(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user
    )

    if request.method == 'POST':
        card.title = request.POST.get('title')
        card.description = request.POST.get('description')
        card.save()

        return redirect('board_detail', board_id=card.task_list.board.id)

    return render(request, 'boards/edit_card.html', {
        'card': card
    })


@login_required
def delete_card(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        task_list__board__owner=request.user
    )

    board_id = card.task_list.board.id

    if request.method == 'POST':
        card.delete()
        return redirect('board_detail', board_id=board_id)

    return render(request, 'boards/delete_card.html', {
        'card': card
    })

@login_required
def edit_board(request, board_id):
    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user
    )

    if request.method == 'POST':
        board.title = request.POST.get('title')
        board.description = request.POST.get('description')
        board.save()

        return redirect('home')

    return render(request, 'boards/edit_board.html', {
        'board': board
    })


@login_required
def delete_board(request, board_id):
    board = get_object_or_404(
        Board,
        id=board_id,
        owner=request.user
    )

    if request.method == 'POST':
        board.delete()
        return redirect('home')

    return render(request, 'boards/delete_board.html', {
        'board': board
    })

@login_required
def edit_list(request, list_id):
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    if request.method == 'POST':
        task_list.title = request.POST.get('title')
        task_list.save()

        return redirect('board_detail', board_id=task_list.board.id)

    return render(request, 'boards/edit_list.html', {
        'task_list': task_list
    })


@login_required
def delete_list(request, list_id):
    task_list = get_object_or_404(
        TaskList,
        id=list_id,
        board__owner=request.user
    )

    board_id = task_list.board.id

    if request.method == 'POST':
        task_list.delete()
        return redirect('board_detail', board_id=board_id)

    return render(request, 'boards/delete_list.html', {
        'task_list': task_list
    })