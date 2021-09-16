from django.shortcuts import render
from .forms import ImageForm
from PIL import Image


def color_count(f):
    img = Image.open(f)
    black = 0
    white = 0
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pix = list(img.getdata())
    hex_pix = [hex((r << 16) + (g << 8) + b) for r, g, b in pix]
    for p in hex_pix:
        if p == '0x0':
            black += 1
        elif p == '0xffffff':
            white += 1
    return white, black


def index(request):
    context = {}

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            colors = color_count(request.FILES['image'])
            context['image'] = request.FILES['image']
            context['white'] = colors[0]
            context['black'] = colors[1]
        else:
            form = ImageForm()
        context['form'] = form

    return render(request=request, template_name='index/index.html', context=context)
