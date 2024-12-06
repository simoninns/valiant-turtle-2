    5 HIMEM=&7A0C
    7ON ERROR GOTO13
   10PROCinitialise
   13 *FX3,0
   14 array=FALSE
   15CLS:PROCheading
   20IFvalid THENPRINTTAB(0,22);STRING$(119," ");
   30PRINTTAB(0,23);STRING$(39," ")
   40PRINTTAB(0,22);STRING$(39," ")
   50PRINTTAB(0,21):c$=FNget_command
   60 IFc$="QUIT"THEN200 
   70IFc$=""THEN20
   80done=FALSE:valid=TRUE
   90PROCprimitive:IFdone THEN180
  100IFc$="EDIT"ORc$="ED"OR c$="TO"THENPROCedit:GOTO180
  110IFc$="PROCS"ORc$="PR"THENPROCprocs:GOTO180
  120IFc$="HELP"THENPROChelp:GOTO180
  130IFc$="SCALE"THENPROCscale:GOTO180
  140IFc$="SAVE"THENPROCsave:GOTO180
  150IFc$="LOAD"THENPROCload:GOTO180
  160IFc$="ERASE"ORc$="ER"THENPROCerase:GOTO180
  170PROCprocess_udp
  180IFvalid THEN30
  190GOTO40
  200PROCfinish
  210IFNOTquit THEN240
  220 *FX154,75
  230 CLS:END
  240CLS:PROCheading:GOTO30
  250DEFFNget_command
  260 *FX154,75
  270INPUTLINEil$:l=LEN(il$):p=0
  280 *FX154,11
  290c$=FNget_next_input_element
  300=c$
  310DEFFNget_next_input_element
  320LOCALj,k
  330IFarray THEN400
  340REPEATp=p+1:UNTILp>l ORMID$(il$,p,1)<>" "
  350j=p-1
  360REPEATj=j+1:UNTILj>l ORMID$(il$,j,1)=" "
  370k=p:p=j
  380word$=MID$(il$,k,j-k)
  390GOTO450
  400PROCwordp
  410IFword$=""THEN450
  420c%(cpoint,1)=xa:c%(cpoint,2)=ya
  430IFLEFT$(word$,1)<>":"THEN450
  440word$=MID$(word$,2):PROCvariable:IFvalid THENword$=STR$(par)
  450=word$
  460DEFFNvalid_param(s$)
  470IF NOTvalid THEN560
  480LOCALi,j,a
  490valid=TRUE
  500IFs$=""THENPRINTTAB(0,23);STRING$(40," "):PRINT TAB(0,23);"ERROR - PARAMETER MISSING":valid=FALSE:GOTO570
  510IFASC(MID$(s$,1,1))<>45THENj=1ELSEj=2
  520FORi=j TOLEN(s$)
  530a=ASC(MID$(s$,i,1))
  540IFa<>46AND(a<48ORa>57)THENvalid=FALSE
  550NEXT
  560IFNOTvalid THENPRINTTAB(0,23);STRING$(39," "):PRINTTAB(0,23);"ERROR - PARAMETER NOT NUMERIC"
  570=valid
  580DEFPROCforward
  590LOCALpar$,d
  600done=TRUE
  610par$=FNget_next_input_element
  620IFNOTFNvalid_param(par$) THEN670
  630d=VAL(par$)
  640nl=ABS(ts*d):nr=nl
  650IFd>0THENdl=1:dr=0ELSEdl=0:dr=1
  660PROCdrive_turtle
  670 ENDPROC
  680DEFPROCbackward
  690LOCALpar$,d
  700done=TRUE
  710par$=FNget_next_input_element
  720IFNOTFNvalid_param(par$) THEN770
  730d=VAL(par$)
  740nl=ABS(ts*d):nr=nl
  750IFd>0THENdl=0:dr=1ELSEdl=1:dr=0
  760PROCdrive_turtle
  770ENDPROC
  780DEFPROCright
  790LOCALpar$,a
  800done=TRUE
  810par$=FNget_next_input_element
  820IFNOTFNvalid_param(par$) THEN870
  830a=VAL(par$)
  840nl=ABS(th*a):nr=nl
  850IFa>0THENdl=1:dr=1ELSEdl=0:dr=0
  860PROCdrive_turtle
  870ENDPROC
  880DEFPROCleft
  890LOCALpar$,a
  900done=TRUE
  910par$=FNget_next_input_element
  920IFNOTFNvalid_param(par$) THEN970
  930a=VAL(par$)
  940nl=ABS(th*a):nr=nl
  950IFa>0THENdl=0:dr=0ELSEdl=1:dr=1
  960PROCdrive_turtle
  970ENDPROC
  980DEFPROCpenup
  990done=TRUE:valid=TRUE
 1000 *FX3,7
 1010pendown=FALSE
 1020A%=0
 1030CALLOSWRCH
 1040PROCdelay(5000)
 1050 *FX3,0
 1060ENDPROC
 1070DEFPROCpendown
 1080done=TRUE:valid=TRUE
 1090 *FX3,7
 1100pendown=TRUE
 1110A%=16
 1120CALLOSWRCH
 1130PROCdelay(5000)
 1140 *FX3,0
 1150ENDPROC
 1160DEFPROCarc
 1170LOCALrad$,ang$,r,a
 1180done=TRUE
 1190rad$=FNget_next_input_element
 1200ang$=FNget_next_input_element
 1210IFNOT(FNvalid_param(rad$) ANDFNvalid_param(ang$))THEN1420
 1220r=VAL(rad$):a=VAL(ang$)
 1230ni=(188.5*ABS(r)-tk)*ABS(a)/360
 1240no=(188.5*ABS(r)+tk)*ABS(a)/360
 1250IFr<0THEN1340
 1260nl=no:nr=ABS(ni)
 1270IFa<0THEN1310
 1280dl=1:dr=0
 1290IFni<0THENdr=1
 1300GOTO1410
 1310dl=0:dr=1
 1320IFni<0THENdr=0
 1330GOTO1410
 1340nl=ABS(ni):nr=no
 1350IFa<0THEN1390
 1360dl=1:dr=0
 1370IFni<0THENdl=0
 1380GOTO1410
 1390dl=0:dr=1
 1400IFni<0THENdl=1
 1410PROCdrive_turtle
 1420ENDPROC
 1430DEFPROChelp
 1440done=TRUE
 1450LOCALx
 1460priname$=FNget_next_input_element
 1470IFLEN(priname$)<1THENpriname$="HELP"
 1480 IFLEN(priname$)<3THENPROCextend_name
 1490 PROCloadscreen
 1500 *FX154,11
 1510 x=GET
 1520 *FX154,75
 1525IFpriname$="H.EDIT"THENpriname$="EDI2":GOTO1490
 1530 CLS:PROCheading
 1540 ENDPROC
 1550DEFPROCdrive_turtle
 1555 IF nl=nr THENGOTO1850:REM NOT ARC
 1560REMsendoutputtoRS423only
 1570 *FX3,7
 1580LOCALinstr_count,slow_prod,next_slow,max_step,max_intervals,min_intervals,instr_remaining,straight,single_skel,both_skel,i,j,delay
 1590instr_count=0:slow_prod=0:next_slow=1:delay=4
 1600IFnr>nl THENmax_step=nr:min_intervals=nl-1ELSEmax_step=nl:min_intervals=nr-1
 1610max_intervals=max_step-1
 1620instr_remaining=max_step
 1650IFnl>nr THENsingle_skel=dl+1+12-pendown*16ELSEsingle_skel=(dr+1)*4+3-pendown*16
 1660both_skel=dl+1+(dr+1)*4+96-pendown*16
 1670A%=15-pendown*16:REMsend instruction to activate motor circuits
 1680CALLOSWRCH
 1690FORi=0TO25:NEXT
 1710REM This section for arcs
 1720FORi=1TOmax_step
 1730A%=both_skel:CALL OSWRCH
 1740slow_prod=slow_prod+max_intervals:next_slow=slow_prod/min_intervals
 1750IFnext_slow>max_step THENnext_slow=max_step
 1760FORj=i+1TOnext_slow:A%=single_skel:CALLOSWRCH:PROCdelay(delay):NEXT
 1770i=next_slow
 1780NEXT
 1810A%=-pendown*16:REM send instruction to switch off motors
 1820CALLOSWRCH
 1830 *FX3,0
 1840GOTO1890
 1850REM STRAIGHT LINE/TURN
 1853data=&0A01 
 1855?data=(-1*pendown):data=data+1
 1860?data=nl MOD 256:data=data+1
 1865?data=nl DIV 256:data=data+1
 1870?data=(dl+1):data=data+1 
 1875?data=(dr+1)
 1880 *FX3,7
 1885 CALL HIMEM+1
 1887 *FX3,0
 1888 FORcounter%=0TO2000:NEXT
 1890 ENDPROC
 1900DEFPROCdelay(x)
 1910LOCALi
 1920FORi=1TOx :NEXT 
 1930ENDPROC
 1940DEFPROCinitialise
 1950CLS:FOR JOE=2TO3:PRINTTAB(3,JOE);CHR$(141);CHR$(130);"VALIANT TURTLE MOVER PROGRAM":NEXT JOE 
 1960PRINTTAB(5,4);" BBC Microcomputer Version"
 1970PRINTTAB(4,7);" (C) Valiant Designs Ltd 1984"
 1980PRINTTAB(2,15);" PLEASE SWITCH ON THE COMMUNICATOR"
 1990PRINTTAB(10,16);" AND THE TURTLE."
 2000PRINTTAB(5,19);" THEN PRESS THE RETURN KEY."
 2010 *FX154,11
 2020X=GET:IFX<>13THENGOTO2020
 2030 PRINTTAB(0,15);STRING$(39," ")
 2040 PRINTTAB(0,16);STRING$(39," ") 
 2050 PRINTTAB(0,19);STRING$(39," ")
 2060 PRINTTAB(12,18);"PLEASE WAIT"
 2070ts=30:th=6:tk=2160
 2080REM Set up RS423 port - set RS423 baud rate t0 4K8
 2090 *FX8,6
 2100 *FX3,7
 2110OSWRCH=&FFEE:REM address of Operating System Write Char routine
 2120A%=13:REM set communicator baud timing
 2130CALLOSWRCH:REM send to communicator
 2140A%=85:REM send check byte
 2150CALLOSWRCH
 2160A%=16:REM send 'PENDOWN' to initialise turtle
 2170pendown=TRUE:valid=TRUE
 2180CALLOSWRCH
 2190CALLOSWRCH
 2200 *FX3,0
 2210PROCdelay(5000)
 2220word=TRUE:array=FALSE:valid=FALSE
 2230DIMs$(3),p$(10),v(31),v$(0),c%(20,5)
 2240psize=10:vsize=1*31:csize=20
 2250FORm=0TO3:s$(m)=STRING$(255," "):NEXT
 2260FORm=0TOpsize:p$(m)=STRING$(255," "):NEXT
 2270v$(0)=STRING$(255," ")
 2280lastx=0:lasty=0
 2290 *FX154,75
 2300ENDPROC
 2310DEFPROCfinish
 2320 CLS:PRINTTAB(14,1);"QUIT"
 2330 PRINTTAB(2,9);"ARE YOU SURE THAT"
 2340 PRINTTAB(2,10);"YOU WANT TO QUIT (YES/NO) ";:c$=FNget_command 
 2350 IFc$<>"YES"THENquit=FALSE:GOTO2370 
 2360 quit=TRUE
 2370ENDPROC
 2380DEFPROCedit
 2390LOCALmaskl,m,n
 2400udp$=FNget_next_input_element
 2410IFLEN(udp$)<1THENPROCerr(40):done=TRUE:GOTO2800
 2420IFNOTFNvalid_name(udp$)THENPROCerr(41):GOTO2800
 2430IFFNfind_udp(udp$)ANDc$="TO"THENPROCerr(60):GOTO2800
 2440maskl=4+LEN(udp$):CLS:updating=FALSE
 2450PRINTTAB(0,24);:VDU 131,157,132;
 2460PRINT"f0 TO DEFINE           f9 TO QUIT":VDU 30
 2470IFFNfind_udp(udp$)THENxa=xa1:ya=ya1:PROCdisp_udp:updating=TRUE:GOTO2510
 2480FORm=0TO3
 2490IFm=0THENs$(0)="TO "+udp$+STRING$(237-LEN(udp$)," "):PRINTLEFT$(s$(0),maskl);ELSEs$(m)=STRING$(240," ")
 2500NEXT
 2510*FX4,1
 2520*FX154,75
 2530*KEY 0 e
 2540*KEY 8 m
 2550c=GET
 2560x=POS:y=VPOS:ll=VPOS:ys=y DIV6:xs1=(y MOD6)*40:xs=xs1+x
 2570IFc=13THENVDU 13:IFy<23THENVDU 10:GOTO2700
 2580IFc=30ORc=94THENVDU 30:GOTO2700
 2590IF(y=0ANDx<maskl)OR(x>38)THEN2630
 2600IFc=92THENs$(ys)=MID$(s$(ys),1,xs)+" "+MID$(s$(ys),xs+1,39-x)+MID$(s$(ys),xs-x+41):PRINTMID$(s$(ys),xs+1,40-x);:PRINTTAB(x,y);:GOTO2700
 2610IFc=127ANDx>0THENs$(ys)=MID$(s$(ys),1,xs-1)+MID$(s$(ys),xs+1,40-x)+" "+MID$(s$(ys),xs-x+41):PRINTTAB(x-1,y);:PRINTMID$(s$(ys),xs,41-x);:PRINTTAB(x-1,y);:GOTO2700
 2620IFc=32OR(c>64ANDc<91)OR(c>47ANDc<59)OR(c=60ORc=62)THENs$(ys)=LEFT$(s$(ys),xs)+CHR$(c)+MID$(s$(ys),xs+2):PRINTTAB(x,y);CHR$(c);:GOTO2700
 2630IFc=101THEN2710
 2640IFc=109THEN2750
 2650IFc=136ANDNOT(x=0ANDy=0)THENVDU8:GOTO2700
 2660IFc=137ANDNOT(x=39ANDy>22)THENVDU9:GOTO2700
 2670IFc=138ANDy<23THENVDU10:GOTO2700
 2680IFc=139ANDy>0THENVDU11:GOTO2700
 2690VDU7
 2700GOTO2550
 2710IFupdating ANDFNfind_udp(udp$)THENPROCdelete
 2720REMIFlasty>=psize-4THENPROCcheckp
 2730IFlasty>=1THENPROCpackp
 2740PROCstore_udp
 2750CLS:PROCheading:done=TRUE
 2755*FX15,1
 2760*FX4,0
 2770*KEY 1
 2780*KEY 8
 2790*FX154,11
 2800ENDPROC
 2810DEFFNvalid_name(udp$)
 2820LOCALm
 2830m=0:REPEATm=m+1:UNTILm>LEN(udp$)ORMID$(udp$,m,1)<"A"ORMID$(udp$,m,1)>"Z"
 2840IFm<=LEN(udp$)THENvalid=FALSE
 2850=valid
 2860DEFFNfind_udp(udp$)
 2870LOCALvalid
 2880valid=FALSE:ya=-1
 2890ya=ya+1:xa=-1
 2900IFya>lasty THEN2970
 2910IFxa>254THEN2890
 2920xa=xa+1:xa=INSTR(p$(ya),"*",xa+1)-1
 2930IFxa<0THEN2890
 2940IFya>=lasty ANDxa>=lastx THEN2970
 2950PROCwordp:IFword$<>udp$THEN2910
 2960valid=TRUE
 2970=valid
 2980DEFPROCheading
 2990CLS:PRINTTAB(14,2);"COMMANDS"
 3000PRINTTAB(4,4);"FORWARD (FD)      BACK    (BK)"
 3010PRINTTAB(4,5);"LEFT    (LT)      RIGHT   (RT)"
 3020PRINTTAB(4,6);"PENUP   (PU)      PENDOWN (PD)"
 3030PRINTTAB(4,7);"SCALE             QUIT"
 3040PRINTTAB(4,8);"EDIT    (ED)      TO"
 3050PRINTTAB(4,9);"PROCS   (PR)      ERASE   (ER)"
 3060PRINTTAB(4,10);"LOAD              SAVE"
 3070PRINTTAB(4,11);"HELP"
 3080PRINTTAB(0,21)
 3090ENDPROC
 3100DEFPROCprimitive
 3110IFc$="FORWARD"ORc$="FD"THENPROCforward
 3120IFc$="BACK"ORc$="BK"THENPROCbackward
 3130IFc$="RIGHT"ORc$="RT"THENPROCright
 3140IFc$="LEFT"ORc$="LT"THENPROCleft
 3150IFc$="PENUP"ORc$="PU"THENPROCpenup
 3160IFc$="PENDOWN"ORc$="PD"THENPROCpendown
 3170IF c$="END"THENdone=TRUE
 3190ENDPROC
 3200DEFPROCerr(err)
 3210PRINTTAB(0,23);STRING$(40," ");
 3220PRINTTAB(0,23);:valid=FALSE
 3230IFerr=0THENPRINT"I don't know how to "+c$;:GOTO3400
 3240IFerr=1THENPRINT"Too many variables used";:GOTO3400
 3250IFerr=2THENPRINT"Invalid procedure name";:GOTO3400
 3260IFerr=3THENPRINT"Unknown variable '"+word$+"' encountered";:GOTO3400
 3270IFerr=10THENPRINT"'REPEAT' command with no number";:GOTO3400
 3280IFerr=12THENPRINT"More than "+STR$(csize)+" nested statements";:GOTO3400
 3290IFerr=13THENPRINT"Can't 'REPEAT' a negative no. of times";:GOTO3400
 3300IFerr=15THENPRINT"No end bracket for 'REPEAT' command";:GOTO3400
 3310IFerr=16THENPRINT"No start bracket for 'REPEAT' command";:GOTO3400
 3320IFerr=20THENPRINT"System problem in udp section";:GOTO3400
 3330IFerr=30THENPRINT"Invalid variable "+word$+" in procedure";:GOTO3400
 3340IFerr=31THENPRINT"Invalid or missing parameter in proc.";:GOTO3400
 3350IFerr=40THENPRINT"Edit what?";:GOTO3400
 3360IFerr=41THENPRINT"Use only 'A' to 'Z' for procedure name";:GOTO3400
 3370IFerr=50THENPRINT"Procedure workspace full";:GOTO3400
 3380IFerr=60THENPRINT"This procedure already exists!";:GOTO3400
 3390PRINT"UNKNOWN ERR - "+STR$(err);
 3400ENDPROC
 3410DEFPROCstore_udp
 3420LOCALm,l,n
 3430xa=lastx:ya=lasty:m=-1
 3440REPEAT:m=m+1
 3450il$=MID$(s$(m DIV6),(m MOD6)*40+1,40)
 3460IFm=0THENil$="*"+MID$(il$,4)
 3470l=LEN(il$):p=0
 3480word$=FNget_next_input_element+" "
 3490IFword$=" "THEN3540
 3500PROCput_word:IFNOTvalid THEN3540
 3510word$=FNget_next_input_element+" "
 3520IFword$<>" "THEN3500
 3530p$(ya)=LEFT$(p$(ya),xa)+"\"+MID$(p$(ya),xa+2)
 3540UNTILm=ll ORNOTvalid
 3550lastx=xa:lasty=ya
 3560 p$(ya)=LEFT$(p$(ya),xa+1)+STRING$(254-xa," ")
 3570ENDPROC
 3580DEFPROCdelete
 3590word$="x\":xa=xa1:ya=ya1
 3600PROCput_word
 3610ENDPROC
 3620DEFPROCput_word
 3630LOCALl,n
 3640l=LEN(word$):n=254-xa:IFn>l THENn=l
 3650p$(ya)=LEFT$(p$(ya),xa+1)+MID$(word$,1,n)+RIGHT$(p$(ya),254-xa-n)
 3660xa=xa+n
 3670IFn>=l THEN3710
 3680IFl>n ANDya>=psize THENPROCerr(50):valid=FALSE:GOTO3710
 3690ya=ya+1:xa=-1
 3700IFl>n THENword$=MID$(word$,n+1):GOTO3640
 3710ENDPROC
 3720DEFPROCwordp
 3730LOCALl,m
 3740word$=""
 3750IFya>lasty OR(ya>=lasty ANDxa>=lastx)THEN3850
 3760xa1=xa:ya1=ya
 3770xa=xa+1
 3780IFxa>254THENxa=0:ya=ya+1
 3790IFMID$(p$(ya),xa+1,1)="*"THEN3850
 3800l=INSTR(p$(ya),"\",xa+1)
 3810IFword THENm=INSTR(p$(ya)," ",xa+1):IFl>m THENl=m
 3820IFl>0THENword$=word$+MID$(p$(ya),xa+1,l-xa-1):xa=l-1:GOTO3850
 3830word$=MID$(p$(ya),xa+1)
 3840xa=255:IFya<psize THENya=ya+1:xa=0:GOTO3800
 3850ENDPROC
 3860DEFPROCdisp_udp
 3870LOCALl,ys,xs,end
 3880word=FALSE:PROCwordp:word=TRUE
 3890word$="TO "+word$
 3900FORl=0TO23
 3910ys=l DIV6:xs=(l MOD6)*40
 3920s$(ys)=LEFT$(s$(ys),xs)+word$+STRING$(255-xs-LEN(word$)," ")
 3930PRINTword$
 3940word=FALSE:PROCwordp:word=TRUE
 3950IFLEN(word$)=0ORLEFT$(word$,1)="*"THENl=23
 3960NEXT
 3970ENDPROC
 3980DEFPROCprocess_udp
 3983 ON ERROR GOTO 4250
 3985IFNOTFNfind_udp(c$)THENPROCerr(0):GOTO4270
 3990c%(0,0)=-1:c%(0,5)=1:cpoint=0
 4000lastx1=lastx:lasty1=lasty:s$(0)="TO xx\"+il$
 4010ll=1:PROCstore_udp:IFNOTvalid THEN4270
 4020IFNOTFNfind_udp("xx")THENPROCerr(20):GOTO4270
 4030c%(0,1)=xa:c%(0,2)=ya
 4040c%(0,3)=xa1:c%(0,4)=ya1
 4050REPEAT
 4060done=FALSE
 4070xa=c%(cpoint,1):ya=c%(cpoint,2)
 4080PROCwordp:IFNOTvalid THEN4240
 4090IFword$=">"ANDc%(cpoint,5)<1THEN4240
 4100IFword$<>">"ANDword$<>""THEN4170
 4110done=TRUE
 4120IFc%(cpoint,5)<2THENcpoint=cpoint-1:GOTO4240
 4130c%(cpoint,1)=c%(cpoint,3)
 4140c%(cpoint,2)=c%(cpoint,4)
 4150c%(cpoint,5)=c%(cpoint,5)-1
 4160GOTO4240
 4170IFRIGHT$(word$,1)<>">"THEN4210
 4180word$=LEFT$(word$,LEN(word$)-1)
 4190xa=xa-2:IFxa<0THENxa=xa+255:ya=ya-1
 4200GOTO3270
 4210IFword$="REPEAT"ORword$="RE"THENPROCrepeat:GOTO 4240
 4220array=TRUE:c$=word$:PROCprimitive:array=FALSE
 4230IFdone THENc%(cpoint,1)=xa:c%(cpoint,2)=ya ELSEPROCudp
 4240UNTILNOTdone ORcpoint<0ORNOTvalid
 4250xa1=c%(0,3):ya1=c%(0,4)
 4260PROCdelete:lastx=lastx1:lasty=lasty1
 4265 ON ERROR GOTO 13
 4270ENDPROC
 4280DEFPROCrepeat
 4290LOCALrline
 4300done=TRUE
 4310PROCwordp:IFword$=""ORword$=":"THENPROCerr(10):GOTO4570
 4320 IF LEFT$(word$,1)<>":" THEN GOTO 4340
 4330word$=MID$(word$,2):PROCvariable:IFNOTvalid THEN4570ELSEGOTO4360
 4340IFNOTFNvalid_param(word$)THEN4570
 4350par=VAL(word$)
 4360IFpar<0THENPROCerr(13):GOTO4570
 4370PROCwordp:IFword$=""THENPROCerr(16):GOTO4570
 4380IFLEFT$(word$,1)<>"<"THENPROCerr(16):GOTO4570
 4390rline=cpoint
 4400IFLEN(word$)=1THEN4430
 4410xa=xa1+1:ya=ya1
 4420IFxa>254THENxa=0:ya=ya+1
 4430IFpar=0THEN4520
 4440IFcpoint>csize THENPROCerr(12):GOTO4570
 4450cpoint=cpoint+1
 4460c%(cpoint,0)=c%(cpoint-1,0)
 4470c%(cpoint,1)=xa
 4480c%(cpoint,2)=ya
 4490c%(cpoint,3)=xa
 4500c%(cpoint,4)=ya
 4510c%(cpoint,5)=par
 4520word=FALSE:PROCwordp:word=TRUE
 4530m=INSTR(word$,">"):IFm<1THENPROCerr(15):GOTO4570
 4540xa=xa1+m+1:ya=ya1
 4550IFxa>254THENxa=xa-255:ya=ya+1
 4560c%(rline,1)=xa:c%(rline,2)=ya
 4570ENDPROC
 4580DEFPROCudp
 4590c%(cpoint,1)=xa:c%(cpoint,2)=ya
 4600IFNOTFNfind_udp(word$)THENPROCerr(0):GOTO4800
 4610done=TRUE
 4620IFcpoint>=csize THENPROCerr(12):GOTO4800
 4630cpoint=cpoint+1:c%(cpoint,0)=c%(cpoint-1,0)
 4640c%(cpoint,1)=xa:c%(cpoint,2)=ya
 4650c%(cpoint,3)=0:c%(cpoint,4)=0:c%(cpoint,5)=0
 4660PROCwordp
 4670IFLEFT$(word$,1)<>":"THENc%(cpoint,1)=xa1:c%(cpoint,2)=ya1:GOTO4800
 4680c%(cpoint,1)=xa:c%(cpoint,2)=ya
 4690PROCvariable:IFNOTvalid THEN4800
 4700cpoint=cpoint-1
 4710xa=c%(cpoint,1):ya=c%(cpoint,2)
 4720PROCwordp:IFword$=""THENPROCerr(31):GOTO4800
 4730c%(cpoint,1)=xa:c%(cpoint,2)=ya
 4740IFLEFT$(word$,1)<>":"THEN4760
 4750word$=MID$(word$,2):PROCvariable:IFNOTvalid THEN4800ELSEGOTO4780
 4760IFNOTFNvalid_param(word$)THENPROCerr(31):GOTO4800
 4770par=VAL(word$)
 4780cpoint=cpoint+1:v(c%(cpoint,0))=par
 4790xa=c%(cpoint,1):ya=c%(cpoint,2):GOTO4660
 4800ENDPROC
 4810DEFPROCvariable
 4820LOCALputting
 4830putting=TRUE
 4840IFLEFT$(word$,1)=":"THENword$=MID$(word$,2)ELSEputting=FALSE
 4850IFLEN(word$)=0THENPROCerr(3):GOTO4890
 4860IFLEN(word$)>8THENPROCerr(2):GOTO4890
 4870word$=word$+STRING$(8-LEN(word$)," ")
 4880IFputting THENPROCput_var ELSEPROCget_var
 4890ENDPROC
 4900DEFPROCput_var
 4910LOCALxv,yv,m
 4920m=c%(cpoint,0)+1:IFm>=vsize THENPROCerr(1):GOTO4960
 4930yv=m DIV31:xv=(m MOD31)*8
 4940v$(yv)=LEFT$(v$(yv),xv)+word$+MID$(v$(yv),xv+9)
 4950c%(cpoint,0)=m
 4960ENDPROC
 4970DEFPROCget_var
 4980LOCALm,yv,xv,w$
 4990m=c%(cpoint,0)+1
 5000m=m-1:yv=m DIV31:xv=m MOD31*8
 5010IFword$=MID$(v$(yv),xv+1,8)THENpar=v(m):GOTO5040
 5020IFm>0THEN5000
 5030PROCerr(3)
 5040ENDPROC
 5050DEFPROCsave
 5060LOCALfilename$,ch,m,xa,ya
 5070filename$=FNget_next_input_element
 5080filename$=LEFT$(filename$,7)
 5090PROCpackp
 5100ch=OPENOUT filename$
 5110PRINT#ch,lastx,lasty
 5120FORm=0TOlasty:PRINT#ch,p$(m):NEXT
 5130CLOSE#ch
 5140ENDPROC
 5150DEFPROCload
 5160LOCALfilename$,ch,filelen
 5170PROCpackp
 5180filename$=FNget_next_input_element
 5190filename$=LEFT$(filename$,6)
 5200ch=OPENUPfilename$
 5210INPUT#ch,lastx,lasty
 5220FORi=0TOlasty:INPUT#ch,p$(i):NEXT
 5230CLOSE#ch
 5240ENDPROC
 5250DEFPROCloadscreen
 5260LOCALch,val,m
 5270priname$="H."+LEFT$(priname$,4)
 5280ch=OPENUPpriname$
 5290FORm=31744TO32767:val=BGET#ch:?m=val:NEXT
 5300CLOSE#ch
 5310ENDPROC
 5320DEFPROCscale
 5330LOCALc,c$
 5340PRINTTAB(0,20);"TURTLE IS MOVING IN UNITS OF ";ts/3;" MM"
 5350PRINTTAB(0,21);"PLEASE ENTER NEW VALUE OR RETURN."
 5360PRINTTAB(0,22);STRING$(40," ")
 5370PRINTTAB(0,22);:c$=FNget_command
 5380c=VAL(c$):IFc=0THEN5400
 5390ts=3*c
 5400PRINTTAB(0,20);STRING$(40," ")
 5410PRINTTAB(0,21);STRING$(40," ")
 5420ENDPROC
 5430DEFPROCprocs
 5440LOCALcount,start
 5450done=TRUE:word=FALSE:xa=0:ya=0:start=FALSE
 5460count=0:CLS:PRINT"DEFINED PROCEDURES"
 5470PROCwordp
 5480IFword$=""AND(ya>lasty OR(ya=lasty ANDxa>=lastx))THEN5550
 5490IFword$=""THENstart=TRUE:GOTO5470
 5500IFstart THENstart=FALSE ELSE GOTO5470
 5510IFLEFT$(word$,1)="x"THEN5470
 5520count=count+1:IFcount MOD25<>0THEN5540
 5530PRINTTAB(0,24);"Press any key to continue":PRINTTAB(0,24);:c=GET
 5540PRINTword$+STRING$(39-LEN(word$)," "):GOTO5470
 5550word=TRUE:PRINTTAB(0,24);"Press any key to exit";:c=GET
 5560CLS:PROCheading
 5570ENDPROC
 5580DEFPROCerase
 5590LOCAL
 5600done=TRUE
 5610udp$=FNget_next_input_element
 5620IFNOTFNfind_udp(udp$)THENPROCerr(2)ELSEPROCdelete 
 5630ENDPROC
 5640 DEFPROCextend_name
 5650 IFpriname$="FD"THENpriname$="FORWARD"
 5660 IFpriname$="BK"THENpriname$="BACK"
 5670 IFpriname$="LT"THENpriname$="LEFT"
 5680 IFpriname$="RT"THENpriname$="RIGHT"
 5690 IFpriname$="PU"THENpriname$="PENUP"
 5700 IFpriname$="PD"THENpriname$="PENDOWN"
 5710 IFpriname$="ER"THENpriname$="ERASE"
 5720 IFpriname$="ED"THENpriname$="EDIT"
 5730 IFpriname$="TO"THENpriname$="EDIT"
 5735 IFpriname$="PR"THENpriname$="PROC"
 5740 ENDPROC
 5750DEFPROCpackp
 5760LOCALxt,yt
 5770IFNOTFNfind_udp("x")THEN5920
 5780off=TRUE
 5790xa=xa+1:IFxa>254THENxa=0:ya=ya+1
 5800IFya>lasty OR(ya=lasty ANDxa>=lastx) THEN5890
 5810IFMID$(p$(ya),xa+1,1)<>"*"THEN5850
 5820xt=xa+1:yt=ya
 5830IFxt>254THENxt=0:yt=yt+1
 5840IFMID$(p$(yt),xt+1,1)="x"THENoff=TRUE ELSEoff=FALSE
 5850IFoff THEN5790
 5860p$(ya1)=LEFT$(p$(ya1),xa1)+MID$(p$(ya),xa+1,1)+MID$(p$(ya1),xa1+2)
 5870xa1=xa1+1:IFxa1>254THENxa1=0:ya1=ya1+1
 5880 GOTO 5790
 5890yt=lasty:lastx=xa1-1:lasty=ya1:IFlastx<0 THENlastx=254:lasty=lasty-1
 5900p$(ya1)=LEFT$(p$(ya1),xa1)+STRING$(255-xa1," ")
 5910xa1=0:ya1=ya1+1:IFya1<=yt THEN5900
 5920ENDPROC

