 def splashscreen(self):
         svg_wid=QSvgWidget()
         svg_wid.setWindowFlags(Qt.WindowType.FramelessWindowHint)
         
         for i in range(101):
             blanc=str(int(255-float(i)/100*255))
             gris=str(int(181-float(i)/100*181))
             svg_txt='<svg width="550px" height="290px">'
             svg_txt+='<defs>'
             svg_txt+='<linearGradient id="grad1" x1="0" y1="0" x2="0" y2="100%">'
             svg_txt+='<stop style="stop-color:#ffffff;stop-opacity:1;" offset="0" />'
             svg_txt+='<stop style="stop-color:#b5b5b5;stop-opacity:1;" offset="1"/>'
             svg_txt+='</linearGradient>'
             svg_txt+='<linearGradient id="grad2" x1="0%" y1="-10%" x2="0" y2="300%">'
             svg_txt+='<stop style="stop-color:rgb(%s,%s,%s);stop-opacity:1" offset="0" />'%(blanc,blanc,blanc)
             svg_txt+='<stop style="stop-color:rgb(%s,%s,%s);stop-opacity:1" offset="1"/>'%(gris,gris,gris)
             svg_txt+='</linearGradient>'
             svg_txt+='</defs>'
             svg_txt+='<rect height="290" width="550" fill="url(#grad1)"/>'
              
             if i<=25:
                 height=float(i)/25*66
                 y1=str(210-height)
                 y2=str(210+height)
                 taille_rouge=str(float(i))
                 stroke_rouge=str(2*6.5*(float(i)/100  ))
                 
                 svg_txt+='<line x1="68" y1="%s" x2="68" y2="%s" stroke="#000000" stroke-width="12"/>' %(y1,y2)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="%s" stroke="#ffffff" stroke-width="%s" fill="#D30000" />' %(taille_rouge,stroke_rouge)
                 
             if 25<i<=50:
                 alpha=(float(i)-25)/25*90
                 alpha_rad=radians(alpha)
                 l1_x1=str(68-44*sin(alpha_rad))
                 l1_x2=str(68+88*sin(alpha_rad))
                 l1_y1=str(188-44*cos(alpha_rad))
                 l1_y2=str(188+88*cos(alpha_rad))
                 taille_rouge=str(float(i))
                 stroke_rouge=str(2*6.5*(float(i)/100  ))
                 
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>' %(l1_x1,l1_y1,l1_x2,l1_y2)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="%s" stroke="#ffffff" stroke-width="%s" fill="#D30000" />' %(taille_rouge,stroke_rouge)
                
             if 50<i<=75:
                 alpha=(float(i)-50)/25*90
                 alpha_rad=radians(alpha)
                 l2_x1=str(112-88*cos(alpha_rad))
                 l2_x2=str(112+44*cos(alpha_rad))
                 l2_y1=str(188+88*sin(alpha_rad))
                 l2_y2=str(188-44*sin(alpha_rad))
                 centre_x_orange=str(220+((float(i)-50)/25*125))
                    
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="24" y1="188" x2="156" y2="188" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>'%(l2_x1,l2_y1,l2_x2,l2_y2)
                 svg_txt+='<circle id="rond_orange" cx="%s" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#FF6E00" />'%(centre_x_orange)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#D30000" />'
                 
             if i>75:
                 alpha=(float(i)-75)/25*90
                 alpha_rad=radians(alpha)
                 l3_x1=str(112-88*sin(alpha_rad))
                 l3_x2=str(112+44*sin(alpha_rad))
                 l3_y1=str(232-88*cos(alpha_rad))
                 l3_y2=str(232+44*cos(alpha_rad))
                 centre_x_vert=str(345+((float(i)-75)/25*125))
                    
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="24" y1="188" x2="156" y2="188" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="112" y1="144" x2="112" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>' %(l3_x1,l3_y1,l3_x2,l3_y2)
                 svg_txt+='<circle id="rond_vert" cx="%s" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#078018" />' %(centre_x_vert)
                 svg_txt+='<circle id="rond_orange" cx="345" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#FF6E00" />'
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#D30000" />'
         
             svg_txt+='<text style="font-size:130px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;fill:url(#grad2);stroke:none;font-family:Sans" x="275" y="110" > ODEGO</text>'
             svg_txt+='</svg>'
             
             svg_bytes = QByteArray(svg_txt.encode())
             svg_wid.load(svg_bytes)
             svg_wid.show()
             QApplication.processEvents()
             time.sleep(0.07)
         time.sleep(0.5)
         svg_wid.close()
