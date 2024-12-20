from django.db.models import Q

def aplicaFiltrosVaga(request):
    if request.method == 'POST':
        descricao = request.POST['filtroDescricao'].strip()
        faixaSalarial = request.POST['filtroFaixaSalarial'].strip()
        escolaridade = request.POST['filtroEscolaridade'].strip()
        modalidade = request.POST['filtroModalidade'].strip()
        indicadorPcd = request.POST['filtroPCD'].strip()
    else:
        descricao = request.GET.get('filtroDescricao', '').strip()
        faixaSalarial = request.GET.get('filtroFaixaSalarial', '0').strip()
        escolaridade = request.GET.get('filtroEscolaridade', '0').strip()
        modalidade = request.GET.get('filtroModalidade', '0').strip()
        indicadorPcd = request.GET.get('filtroPCD', '0').strip()

    filtros = Q(descricao__icontains=descricao)
    filtros &= Q(ativo=True)
    if faixaSalarial != '0':
        filtros &= Q(faixaSalarial=int(faixaSalarial))

    if escolaridade != '0':
        filtros &= Q(escolaridade=int(escolaridade))

    if modalidade != '0':
        filtros &= Q(modalidade=int(modalidade))

    if indicadorPcd != '0':
        filtros &= Q(indicadorPCD=bool(indicadorPcd))

    return filtros

def filtrosVaga(request):
    if request.method == 'POST':
        descricao = request.POST['filtroDescricao'].strip()
        faixaSalarial = request.POST['filtroFaixaSalarial'].strip()
        escolaridade = request.POST['filtroEscolaridade'].strip()
        modalidade = request.POST['filtroModalidade'].strip()
        indicadorPcd = request.POST['filtroPCD'].strip()
    else:
        descricao = request.GET.get('filtroDescricao', '').strip()
        faixaSalarial = request.GET.get('filtroFaixaSalarial', '0').strip()
        escolaridade = request.GET.get('filtroEscolaridade', '0').strip()
        modalidade = request.GET.get('filtroModalidade', '0').strip()
        indicadorPcd = request.GET.get('filtroPCD', '0').strip()
    return {
        'filtroDescricao':descricao,
        'filtroFaixaSalarial':int(faixaSalarial),
        'filtroEscolaridade':int(escolaridade),
        'filtroModalidade':int(modalidade),
        'filtroIndicadorPcd':indicadorPcd
    }
