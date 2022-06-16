import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import ConsultaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import AgendarCita, Persona, Odontograma, Consulta


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_atender_cita(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    usuario_logeado = request.user
    if Persona.objects.filter(usuario=usuario_logeado, status=True).exists():
        persona_logeado = Persona.objects.get(usuario=usuario_logeado, status=True)
    else:
        persona_logeado = 'SUPERADMINISTRADOR'
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'atender_consulta':
                try:
                    form = ConsultaForm(request.POST, request.FILES)
                    if form.is_valid():
                        colores = request.POST.getlist('color[]')
                        partes = request.POST.getlist('identificador[]')
                        odontograma = Odontograma(TP18=colores[0], BP18=colores[1],
                                                  RP18=colores[2], LP18=colores[3], CP18=colores[4], CP17=colores[5],
                                                  TP17=colores[6], BP17=colores[7], RP17=colores[8], LP17=colores[9],
                                                  CP16=colores[10], TP16=colores[11], BP16=colores[12],
                                                  RP16=colores[13],
                                                  LP16=colores[14], CP15=colores[15], TP15=colores[16],
                                                  BP15=colores[17],
                                                  RP15=colores[18], LP15=colores[19], CP14=colores[20],
                                                  TP14=colores[21],
                                                  BP14=colores[22], RP14=colores[23], LP14=colores[24],
                                                  CP13=colores[25],
                                                  TP13=colores[26], BP13=colores[27], RP13=colores[28],
                                                  LP13=colores[29],
                                                  CP12=colores[30], TP12=colores[31], BP12=colores[32],
                                                  RP12=colores[33],
                                                  LP12=colores[34], CP11=colores[35], TP11=colores[36],
                                                  BP11=colores[37],
                                                  RP11=colores[38], LP11=colores[39], CP55=colores[40],
                                                  TP55=colores[41],
                                                  BP55=colores[42], RP55=colores[43], LP55=colores[44],
                                                  CP54=colores[45],
                                                  TP54=colores[46], BP54=colores[47], RP54=colores[48],
                                                  LP54=colores[49],
                                                  CP53=colores[50], TP53=colores[51], BP53=colores[52],
                                                  RP53=colores[53],
                                                  LP53=colores[54], CP52=colores[55], TP52=colores[56],
                                                  BP52=colores[57],
                                                  RP52=colores[58], LP52=colores[59], CP51=colores[60],
                                                  TP51=colores[61],
                                                  BP51=colores[62], RP51=colores[63], LP51=colores[64],
                                                  CP85=colores[65],
                                                  TP85=colores[66], BP85=colores[67], RP85=colores[68],
                                                  LP85=colores[69],
                                                  CP84=colores[70], TP84=colores[71], BP84=colores[72],
                                                  RP84=colores[73],
                                                  LP84=colores[74], CP83=colores[75], TP83=colores[76],
                                                  BP83=colores[77],
                                                  RP83=colores[78], LP83=colores[79], CP82=colores[80],
                                                  TP82=colores[81],
                                                  BP82=colores[82], RP82=colores[83], LP82=colores[84],
                                                  CP81=colores[85],
                                                  TP81=colores[86], BP81=colores[87], RP81=colores[88],
                                                  LP81=colores[89],
                                                  CP48=colores[90], TP48=colores[91], BP48=colores[92],
                                                  RP48=colores[93],
                                                  LP48=colores[94], CP47=colores[95], TP47=colores[96],
                                                  BP47=colores[97],
                                                  RP47=colores[98], LP47=colores[99], CP46=colores[100],
                                                  TP46=colores[101],
                                                  BP46=colores[102], RP46=colores[103], LP46=colores[104],
                                                  CP45=colores[105], TP45=colores[106], BP45=colores[107],
                                                  RP45=colores[108], LP45=colores[109], CP44=colores[110],
                                                  TP44=colores[111], BP44=colores[112], RP44=colores[113],
                                                  LP44=colores[114], CP43=colores[115], TP43=colores[116],
                                                  BP43=colores[117], RP43=colores[118], LP43=colores[119],
                                                  CP42=colores[120], TP42=colores[121], BP42=colores[122],
                                                  RP42=colores[123], LP42=colores[124], CP41=colores[125],
                                                  TP41=colores[126], BP41=colores[127], RP41=colores[128],
                                                  LP41=colores[129], CP21=colores[130], TP21=colores[131],
                                                  BP21=colores[132], RP21=colores[133], LP21=colores[134],
                                                  CP22=colores[135], TP22=colores[136], BP22=colores[137],
                                                  RP22=colores[138], LP22=colores[139], CP23=colores[140],
                                                  TP23=colores[141], BP23=colores[142], RP23=colores[143],
                                                  LP23=colores[144], CP24=colores[145], TP24=colores[146],
                                                  BP24=colores[147], RP24=colores[148], LP24=colores[149],
                                                  CP25=colores[150], TP25=colores[151], BP25=colores[152],
                                                  RP25=colores[153], LP25=colores[154], CP26=colores[155],
                                                  TP26=colores[156], BP26=colores[157], RP26=colores[158],
                                                  LP26=colores[159], CP27=colores[160], TP27=colores[161],
                                                  BP27=colores[162], RP27=colores[163], LP27=colores[164],
                                                  CP28=colores[165], TP28=colores[166], BP28=colores[167],
                                                  RP28=colores[168], LP28=colores[169], CP61=colores[170],
                                                  TP61=colores[171], BP61=colores[172], RP61=colores[173],
                                                  LP61=colores[174], CP62=colores[175], TP62=colores[176],
                                                  BP62=colores[177], RP62=colores[178], LP62=colores[179],
                                                  CP63=colores[180], TP63=colores[181], BP63=colores[182],
                                                  RP63=colores[183], LP63=colores[184], CP64=colores[185],
                                                  TP64=colores[186], BP64=colores[187], RP64=colores[188],
                                                  LP64=colores[189], CP65=colores[190], TP65=colores[191],
                                                  BP65=colores[192], RP65=colores[193], LP65=colores[194],
                                                  CP71=colores[195], TP71=colores[196], BP71=colores[197],
                                                  RP71=colores[198], LP71=colores[199], CP72=colores[200],
                                                  TP72=colores[201], BP72=colores[202], RP72=colores[203],
                                                  LP72=colores[204], CP73=colores[205], TP73=colores[206],
                                                  BP73=colores[207], RP73=colores[208], LP73=colores[209],
                                                  CP74=colores[210], TP74=colores[211], BP74=colores[212],
                                                  RP74=colores[213], LP74=colores[214], CP75=colores[215],
                                                  TP75=colores[216], BP75=colores[217], RP75=colores[218],
                                                  LP75=colores[219], CP31=colores[220], TP31=colores[221],
                                                  BP31=colores[222], RP31=colores[223], LP31=colores[224],
                                                  CP32=colores[225], TP32=colores[226], BP32=colores[227],
                                                  RP32=colores[228], LP32=colores[229], CP33=colores[230],
                                                  TP33=colores[231], BP33=colores[232], RP33=colores[233],
                                                  LP33=colores[234], CP34=colores[235], TP34=colores[236],
                                                  BP34=colores[237], RP34=colores[238], LP34=colores[239],
                                                  CP35=colores[240], TP35=colores[241], BP35=colores[242],
                                                  RP35=colores[243], LP35=colores[244], CP36=colores[245],
                                                  TP36=colores[246], BP36=colores[247], RP36=colores[248],
                                                  LP36=colores[249], CP37=colores[250], TP37=colores[251],
                                                  BP37=colores[252], RP37=colores[253], LP37=colores[254],
                                                  CP38=colores[255], TP38=colores[256], BP38=colores[257],
                                                  RP38=colores[258], LP38=colores[259])

                        odontograma.save(request)



                        cita = AgendarCita.objects.get(pk=request.POST['id'])
                        cita.estado_cita = 1
                        cita.save(request)

                        consulta = Consulta(
                            paciente=cita.paciente,
                            doctor=cita.doctor,
                            diagnostico_previo=form.cleaned_data['diagnostico_previo'],
                            odontograma=odontograma,
                            observacion=form.cleaned_data['observacion'],
                        )
                        consulta.save(request)

                        for foo in form.cleaned_data['tratamientos']:
                            consulta.tratamientos.add(foo)


                    '''
                    #realizar el guardado de la consulta - diagnostico previo - tratamiento y odontograma
                    '''

                    return JsonResponse({"respuesta": True, "mensaje": "Se registro correctamente la consulta."})
                except Exception as ex:
                    pass



            if peticion == 'anular_cita':
                try:
                    with transaction.atomic():
                        registro = AgendarCita.objects.get(pk=request.POST['id'])
                        registro.estado_cita = 3
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Cita anulada correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'atender_consulta':
                try:
                    data['titulo'] = 'Consulta'
                    data['titulo_formulario'] = 'Formulario de atención de consulta a paciente'
                    data['peticion'] = 'atender_consulta'
                    data['persona_logeado'] = persona_logeado
                    data['cita'] = cita =AgendarCita.objects.get(pk=request.GET['id'])
                    form2 = ConsultaForm()
                    data['form2'] = form2
                    return render(request, "atender_cita/consulta.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Citas Planificadas'
                data['titulo_tabla'] = 'Lista  de citas'
                data['persona_logeado'] = persona_logeado
                if not persona_logeado =='SUPERADMINISTRADOR':
                    lista = AgendarCita.objects.filter(status=True,doctor__persona= persona_logeado ).order_by('-estado_cita')
                else:
                    lista = AgendarCita.objects.filter(status=True).order_by('fecha')

                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj

                return render(request, "atender_cita/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
