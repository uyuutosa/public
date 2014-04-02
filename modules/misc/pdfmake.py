
def pdfmake(name,PICPATHLIST,comment):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    PDFPATH=name
    pdf_data = canvas.Canvas(PDFPATH)
    pdf_data.setPageSize((21.0*cm,29.7*cm))
    
    
    pics=[
        [30,650,0],
        [220,650,0],
        [400,650,0],
        [30,522,0],
        [220,522,0],
        [400,522,0],
        [30,394,0],
        [220,394,0],
        [400,394,0],
        [30,266,0],
        [220,266,0],
        [400,266,0],
        [30,138,0],
        [220,138,0],
        [400,138,0],
        [30,10,0],
        [220,10,0],
        [400,10,0]
        ]
    
    i=0    

    for name in PICPATHLIST:
        print name
        if type(name) == str:
            pics[i][2]=name
        i+=1
        
    
    
    
    for pic in pics:
        print pic

        if type(pic[2]) == str:
    #        pdf_data.drawInlineImage(pic[2],0,10*cm,width=9.0*cm, height=3*cm)
            pdf_data.drawInlineImage(pic[2],pic[0],pic[1],width=6*cm, height=4.5*cm)
    st1=comment
    #st1="grep time="+gtime+"[msec]"
    #st2=LBHC[1:-1]
    #st3=LBM[1:-1]
    #st4=LBL[1:-1]
    #st5=TPL[1:-1]
    #st6=MPA[1:-1]
    #st7=MPL[1:-1]
    #st8="Coordination="+coordination
    #st9=shot
    pdf_data.drawString(1*cm,29*cm,st1)
    #pdf_data.drawString(10*cm,29*cm,st2)
    #pdf_data.drawString(1*cm,28.5*cm,st3)
    #pdf_data.drawString(10*cm,28.5*cm,st4)
    #pdf_data.drawString(1*cm,28*cm,st5)
    #pdf_data.drawString(10*cm,28*cm,st6)
    #pdf_data.drawString(1*cm,27.5*cm,st7)
    #pdf_data.drawString(10*cm,27.5*cm,st8)
    #pdf_data.drawString(10*cm,26.5*cm,st9)
    pdf_data.showPage()
    pdf_data.save()
    return PDFPATH
