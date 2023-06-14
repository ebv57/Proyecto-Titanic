
#-------------------LIBRERIAS-----------------------#
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image #Para poder leer las imagenes jpg
import base64 #Para el gif
import io #Para ver la df.info()
#-------------------LIBRERIAS-----------------------#


#-------------------CONFIGURACIÓN-----------------------#
#Hay dos opciones de layout, wide or centered:
st.set_page_config(page_title = 'Titanic Project', page_icon = '🚢', layout='wide')
# Para que a la gente que use el codigo no le aparezcan los warnings de cambios en las librerias ponemos:
st.set_option('deprecation.showPyplotGlobalUse', False)
#-------------------CONFIGURACIÓN-----------------------#



#-------------------COSAS QUE VAMOS A USAR EN TODA LA APP-----------------------#
#opening the image
image1 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\mapa.jpg')
image2 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\joseph-bruce-owner.jpg')
image3 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\capitan_.jpg')
image4 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\Millvina1.jpg')
image5 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\millvina_news.jpg')
image6 = Image.open(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\Cave_list.jpg')

# gif from local file
#Gif Info
file_ = open(r"C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\jackyrose.gif", "rb")
contents = file_.read()
data_url1 = base64.b64encode(contents).decode("utf-8")
file_.close()

#Gif conclusiones
file_2 = open(r"C:\Users\User\Documents\GitHub\Proyecto-Titanic\img\titanic-band.gif", "rb")
contents2 = file_2.read()
data_url2 = base64.b64encode(contents2).decode("utf-8")
file_2.close()


#Dataframes
df = pd.read_csv(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\data\titanic.csv')

df1=df.copy() # Se hace una copia para trabajar sobre la copia y limpiar los datos sobre esta
#------------Limpieza de datos-----------#
# Sustituimos valores nulos de edad por mediana:
df1['Age'] = df1['Age'].fillna(df1['Age'].median())
# Sustituimos valores nulos de Cabin por '00':
df1['Cabin'] = df1['Cabin'].fillna('00')
# Sustituimos valores nulos de embarked por la moda:
df1['Embarked'] = df1['Embarked'].fillna(df1['Embarked'].mode().iloc[0])
#------------Limpieza de datos-----------#

#Análisis cabinas con los Cardeza:
df_cabin=df.loc[df['Name'].str.contains('Martinez')]
df_cabin_00=df1.loc[df1['Cabin']=='00'].sort_values('Pclass', ascending=True)

# Análisis de los Dean (pestaña 3):
df_edad_min = df.loc[df['Survived'] == 1].sort_values('Age', ascending=True)
df_filtrado = df_edad_min[df_edad_min['Name'].str.contains('Dean')]
df_filtrado_Dean=df[df['Name'].str.contains('Dean')]
df_filtrado_Light=df[df['Name'].str.contains('Light')]

#Para el grafico de puertos de embarque:
embarked_counts = df1['Embarked'].value_counts().sort_index()

# Tabla excel hecha por mi conversión precios (pestaña 3):
dfex1 = pd.read_excel(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\data\fare_titanic.xlsx',sheet_name='1912')
dfex2 = pd.read_excel(r'C:\Users\User\Documents\GitHub\Proyecto-Titanic\data\fare_titanic.xlsx',sheet_name='Actualidad')
# Calculo de media de precios por clase:
df1_mean_fare = df1.groupby(['Pclass'])['Fare'].mean()

#-------------------COSAS QUE VAMOS A USAR EN TODA LA APP-----------------------#


#--------------------gráficas----------------------------#
fig1= px.histogram(df, x="Age", color="Survived", title="Distribución de la edad")
fig2 = go.Figure(go.Bar(x=embarked_counts.index, y=embarked_counts.values, text=embarked_counts.values, textposition='auto'))
fig2.update_layout(title='Pasajeros por puerto de embarque en el Titanic', xaxis_title='Puerto', yaxis_title='Cantidad de pasajeros')
fig3 = px.scatter(df1, x="Age", y="Fare", color="Cabin")

#--------------------gráficas----------------------------#



#-------------------TITLE-----------------------#
st.title('ANÁLISIS SOBRE EL TITANIC')
#-------------------TITLE-----------------------#


#-------------------pestañas---------------------------#
# Las pestañas aparecen como menu:
tab1, tab2 , tab3, tab4, tab5 = st.tabs(["Info", "Cleaning Data", "Análisis","Conclusiones", "Bibliografía"])

#----------------------------------------------PESTAÑA 1---------------------------------------------------------#
with tab1:
#Info general y personas a bordo:

#Imagen centrada, añado tantas columnas como vea para que quede centrada, depende de la pantalla en la que vea el streamlit:

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(' ')

    with col2:
        st.image(image1, width=800)

    with col3:
        st.write(' ')
    with col4:
        st.write(' ')
    with col5:
        st.write(' ')
      
#Texto  
    #Titulo:
    st.header('El Titanic:')
    #Intro. Para que quedará centrado y pueda editar el texto en según que ocasiones se utiliza lenguaje html:
    st.markdown("""<span style='text-align: center; color: black;'>Cuatro días después de zarpar de Southampton, el Titanic chocó contra un iceberg y se hundió:   
                    - Murieron 1.500 personas y 700 sobrevivieron.  
                    - Era el **barco más grande del mundo**.  
                    - Se hundió en su **viaje inaugural**.  
                    - Su **capitán recibió muchos avisos de hielo** en la ruta, pero no redujo la velocidad.  
                    - **No había suficientes botes salvavidas** para toda la gente a bordo.  
                    - Muchos tripulantes y pasajeros perdieron la vida, pero **el propietario del Titanic sobrevivió** (Joseph Bruce Ismay).  
                    - Entre los pasajeros y la tripulación había **tanto millonarios** como personas en situación de **extrema pobreza**, y nos han quedado muchas historias fascinantes de sus vidas.</h2>""", unsafe_allow_html=True)
    #Sección de pasajeros que quiero destacar porque me parecen interesantes:
    st.header('Pasajeros destacables:')    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('**Joseph Bruce Ismay**')
        st.image(image2, width=250)
        st.write('''💰**Presidente y director** de White Star Line,a naviera que había dado vida al Titanic.
                 Viajaba a bordo del barco y **sobrevivió** a su hundimiento, pero a causa de esto se convirtió en el blanco de todas las críticas.''')
    with col2:
        st.write('**Edward John Smith**')
        st.image(image3, width=250)
        st.write('''🛳️**Capitán del Titanic**. Antes de capitanear el Titanic, había comandado el Republic, Coptic, Majestic, Baltic, Adriatic y el Olympic.
                 Miembro de la Royal Naval Reserve.
                 **Murió ahogado durante el hundimiento** y su cuerpo no fue recuperado.''')
    with col3:
        st.write('**Elizabeth Gladys "Millvina" Dean**')
        st.image(image4, width=250)
        st.write('''👶**Última superviviente** del hundimiento del Titanic.
                 También era **la más joven** de los pasajeros, 
                 ya que tenía apenas dos meses y trece días de edad en el momento que embarcó junto a su familia.''')
    
    st.header('Jack y Rose:') 
    st.markdown("""<span style='text-align: center; color: black;'>Jack y Rose son personajes ficticios y por lo tanto no fueron pasajeros del Titanic.👩‍❤️‍👨🎻😭</h2>""", unsafe_allow_html=True)
    # Parece ser que actualmente st.image solo soporta PNG y JPG, asi que hemos definido más arriba una función para leer el GIF y así se vería:
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url1}" alt="cat gif">',
        unsafe_allow_html=True,
    ) 
#----------------------------------------------PESTAÑA 1---------------------------------------------------------#  

#----------------------------------------------PESTAÑA 2---------------------------------------------------------#     
with tab2:

    #-------DataFrame----------#
    st.subheader('DataFrame:')
    st.dataframe(df, hide_index=True)
    #-------DataFrame----------#   
    
    #-------DataFrame.info----------# 
    st.subheader('Análisis del dataset:')
    st.write('Si aplicamos df.info() el dataframe nos da la siguiente información:')
    # Hay que meter este codigo para que se vea df.info:
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    st.write('Aquí vemos que hay 3 variables con valores nulos y que también hay variables tipo "objeto" que deberían de ser string')
    st.write('''En el dataset hay un  8% de valores nulos y un un  25% de columnas con al menos 1 valor nulo:    
              
            Valores_nulos_porcentaje =  (866/(891*12))*100
    Filas_con_valores_nulos_porc =  3/(12))*100''')
    
    #-------Composición Valores nulos----------#
    
    # Gráfico de quesitos o 'pie chart'
    null_columns = df.columns[df.isnull().any()] #df.isnull().any() indica qué columnas tienen al menos un valor nulo.
    df_nulls = df[null_columns]
    # Dataframe para el grafico:
    values = df_nulls.isnull().sum()
    names = null_columns

    df_pie = pd.DataFrame({'values': values, 'names': names})

    # Pie chart:
    fig = px.pie(df_pie, values='values', names='names',title='Composición de los valores nulos:',color='names',
                color_discrete_map={'Cabin':'cyan',
                                    'Age':'lightcyan',
                                    'Embarked':'darkblue',
                                    })
    # En vez de usar fig.show() como estamos en streamlit utilizamos:
    st.plotly_chart(fig, use_container_width=True)
    
    #-------Composición Valores nulos----------#
    st.header('Método aplicado para sustituir los valores nulos:')
    st.markdown("""<span style='text-align: center; color: black;'>Para poder sustituir los valores nulos veremos que distribución siguen esas variables.  
    - Si la distribución es :green[simétrica] y los valores numéricos lo sustituiremos por la :green[media].  
    - Si la distribución es :red[asimétrica] utilizaremos la :red[mediana].  
    - Si los valores son :blue[categóricos] o tienen pocos valores únicos utilizaremos la :blue[moda].  
    </h2>""", unsafe_allow_html=True)
    
    #-------AGE----------#
    st.subheader('**Variable Age**')
    st.markdown("""<span style='text-align: center; color: black;'>Vemos en el siguiente histograma que la variable edad sigue una distribución :red[asimétrica] sesgada por la derecha por lo tanto utilizaremos la mediana para sustituir los valores nulos. </h2>""", unsafe_allow_html=True)
    # Histograma definido arriba    
    st.plotly_chart(fig1)
    
    st.write('**Aplicaremos el siguiente codigo para rellenar los valores nulos:**')
    st.markdown("""<span style='text-align: center; color: violet;'>df1['Age'] = df1['Age'].fillna(df1['Age'].median()) </h2>""", unsafe_allow_html=True)
    

    #-------AGE----------#
    
    #-------EMBARKED----------#
    st.subheader('**Variable Embarked**')
    st.markdown("""<span style='text-align: center; color: black;'>Como el número de los :blue[valores únicos] (para saber que valores únicos tiene utilizamos la función unique para ver los valores únicos que tiene: 
                df['Embarked'].unique())de Embarked es reducido aplicaremos la moda. </h2>""", unsafe_allow_html=True)    
    
    st.write('**Aplicaremos el siguiente codigo para rellenar los valores nulos:**')
    st.write('Accedemos al valor modal directamente con el índice 0.')
    st.markdown("""<span style='text-align: center; color: violet;'>df1['Embarked'] = df1['Embarked'].fillna(df1['Embarked'].mode().iloc[0]) </h2>""", unsafe_allow_html=True)
    df['Embarked'].unique()
    

    #-------EMBARKED----------#
    
    #-------CABIN----------#
    st.subheader('**Variable Cabin**')
    st.markdown("""<span style='text-align: center; color: black;'>A la variable "Cabin" le **faltan más del 50% de los datos** así que, en principio, se rellenan los valores nulos con '00' y no se utilizará para análisis posteriores. </h2>""", unsafe_allow_html=True)    
    
    st.write('**Aplicaremos el siguiente codigo para rellenar los valores nulos:**')
    st.markdown("""<span style='text-align: center; color: violet'>df1['Cabin'] = df1['Cabin'].fillna('00')]. </h2>""", unsafe_allow_html=True)

    st.write('''Lo correcto habría sido analizar los nombres de los que no cuentan con cabina y relacionarlos con familiares, amigos... porque algunos aparecen 
                con varias cabinas. Por ejemplo, Miss. Anna Ward era la asistenta de Mrs James Warburton Martinez Cardeza.
                Vemos que Cardeza tiene muchas cabinas contratadas en el siguiente dataframe:''')
    st.dataframe(df_cabin, hide_index=True)
    st.write('El siguiente dataframe muestra las personas sin cabina ordenadas por clase. Podemos ver a Miss Anna Ward entre ellos:')
    st.dataframe(df_cabin_00, hide_index=True)


    #-------CABIN----------#
    
    #-------ASTYPE----------#
    st.header('Variables tipo "object":')
    df1 = df1.convert_dtypes()
    st.write('**Aplicaremos el siguiente codigo para rellenar los valores nulos:**')
    st.markdown("""<span style='text-align: center; color: violet;'>df1 = df1.convert_dtypes() </h2>""", unsafe_allow_html=True)
    
    st.write('**Aquí vemos que se han solucionado tanto los problemas de valores nulos como los valores de tipo objeto que ahora aparecen como string:**')
    
    buffer = io.StringIO()
    df1.info(buf=buffer)
    s = buffer.getvalue()

    st.text(s)
    #-------ASTYPE----------#



#----------------------------------------------PESTAÑA 2---------------------------------------------------------#
#----------------------------------------------PESTAÑA 3---------------------------------------------------------# 
with tab3:
    tab1, tab2 , tab3 = st.tabs(["👨‍👩‍👧‍👦", "⚓", "💲"])
    with tab1:   
        st.subheader('Analizando a la familia Dean:')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')

        with col2:
            st.image(image5, width=500)

        with col3:
            st.write(' ')

        st.write(' ')    
        st.write('''Como hemos podido ver al inicio uno de los personajes interesantes a destacar es Millvina Dean.  
                A continuación vamos a navegar dentro de los datos para encontrar a los hermanos Dean a partir del dataframe ordenado por edad de menor a mayor y 
                filtrando por supervivientes, ya que tanto ella como su hermano sobrevivieron: 
                **Millvina Dean y Bertram Vere Dean**.  
                Para ello hemos definido el siguiente dataframe: :violet[df_edad_min = df.loc[df['Survived'] == 1].sort_values('Age', ascending=True)]''')
        st.dataframe(df_edad_min, hide_index=True)
        
        st.write("A primera vista no aparecen en la lista, filtramos entonces por el apellido Dean (:violet[df_filtrado = df_edad_min[df_edad_min['Name'].str.contains('Dean')]]):")
        st.dataframe(df_filtrado, hide_index=True)
        
        st.write('Parece que Millvina era tan pequeña que no aparece, pero su hermano mayor si. Vamos a ver si aparecen su padre y su madre Bertram Frank Dean y Eva Georgette Light:')
        st.write('Primero si seleccionamos por "Dean":')
        st.dataframe(df_filtrado_Dean, hide_index=True)
        st.write('Si que aparece el padre (y el hijo otra vez).')
        st.write('Si buscamos a la madre por el apellido o por el nombre:')    
        st.dataframe(df_filtrado_Light, hide_index=True)
        st.write('''Vemos que no aparece en el dataset, pero sabemos que si que embarcó y sobrevivió con sus dos hijos.  
                 El marido, sin embargo, perdió la vida salvando a su hijo.''')
    
    with tab2:
        st.subheader('Comparando los datos con los certificados de embarque:')
        st.write('''Los certificados de embarque del Titanic indican que 922 pasajeros embarcaron en Southampton, 274 en Cherbourg  y 120 en Queenstown, lo que da al Titanic un total de 1316 pasajeros.  
                            Vamos a analizar cuantos pasajeros embarcaron de cada puerto según nuestros datos:''')
        #Gráfico de barras puertos de embarque:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')

        with col2:
            st.plotly_chart(fig2)

        with col3:
            st.write(' ')
        
        st.write('Los datos no coinciden con los certificados de embarque.')
    with tab3: 
    #Análisis tarifas y tickets
        st.subheader('Analizando los precios')

        st.write('''En la siguiente tabla con datos reales de fuentes externas podemos ver los precios de los billetes tanto en libras, 
                dolares como en euros del año de la inauguración, 1912, y en la actualidad:''')
        st.subheader('Tarifas de 1912 vs actualidad:')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(' ')
        with col2:
            st.dataframe(dfex1, hide_index=True)

        with col3:
            st.dataframe(dfex2, hide_index=True)
        with col4:
            st.write(' ')

        st.write('''Como se puede ver los precios son muy variopintos. Vamos a compararlos con la media de los precios agrupados por clase del dataframe:  
             ''')
        
        st.dataframe(df1_mean_fare)
        
        st.write('''Como podemos ver hay diferencias importantes. Habría que analizar en profundidad la fuente de la tabla de los datos reales y no olvidemos que como hemos visto en el análisis de los puertos de embarque faltan muchos datos de pasajeros en el dataset.  
                 A continuación vamos a ver la dispersión de los datos según la edad de los pasajeros y la cabina:''')
        #Scatter chart
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')

        with col2:
            st.plotly_chart(fig3)

        with col3:
            st.write(' ')
            
        st.write('''Al parecer la cabina más cara que aparece ahí no coincide con la del dueño, Mr Joseph Bruce Ismay, quién declaró frente al Senado:  
                 "B-52 is the room I had."  
                 "You had the suite?"  
                 " I had the suite."  
                 El origen de la escasez de datos de los camarotes se debe a que la única prueba documental que apareció sobre la asignación de camarotes se encontró en el cuerpo del camarero Herbert Cave,
                 entre sus efectos personales se encontró una lista parcial a la que se denominaría "Cave List":''')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')

        with col2:
            st.image(image6, width=500)

        with col3:
            st.write(' ')
            
    
# ----------------------------------------------PESTAÑA 3---------------------------------------------------------# 


#----------------------------------------------PESTAÑA 4---------------------------------------------------------#        
with tab4:

    st.subheader('Conclusiones sobre el dataset:')
    st.write('''  
                     En este dataset como hemos podido ver con **df.info()** hay 891 ID de pasajeros.  
                     Hay pasajeros que se encontraban en la embarción que no cuentan con ID porque 
                     aparecen indicados como parientes de un familiar que si que figura con ID,
                     como hemos podido ver con el caso de la familia Dean, en la que sólo aparecen el hijo mayor y el marido de Eva, pero no aparecen ni ella ni su hija.  
                     No obstante, también es posible que falten datos por otras razones como por ejemplo: por la pérdida de los datos en el hundimiento (como los datos de los camarotes), porque igual no todos los pasajeros con billete llegaron a embarcar...   
                     Por esa razón no se ha elegido hacer correlaciones o rectas de regresión porque sin la totalidad de los datos esos resultados no iban a tener fiabilidad,
                     se ha obtado por hacer una análisis más descriptivo.  
                     En mi opinión sería posible con más tiempo, documentación sobre los pasajeros y con técnicas más avanzadas poder ir completando los datos faltantes, pero con estos datos  
                     no podemos obtener una conclusión clara ni extrapolable a todos los pasajeros del Titanic porque no contamos con toda la información. ''')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')

    with col2:
        st.markdown(
        f'<img src="data:image/gif;base64,{data_url2}" alt="cat gif">',
        unsafe_allow_html=True,
        ) 

    with col3:
        st.write(' ')
    
#----------------------------------------------PESTAÑA 4---------------------------------------------------------#      
    

    

#----------------------------------------------PESTAÑA 5---------------------------------------------------------#     
with tab5:
    st.title('Bibliografía')
    st.write('''
             Info. personas a bordo:  
             https://kids.britannica.com/kids/article/Titanic/353863
             https://www.encyclopedia-titanica.org/titanic/#why-titanic-famous
             https://www.nationalgeographic.es/historia/edward-john-smith-capitan-del-titanic#:~:text=Antes%20de%20capitanear%20el%20Titanic,su%20cuerpo%20no%20fue%20recuperado.
             https://historia.nationalgeographic.com.es/a/vidas-truncadas-titanic_11387
             https://es.wikipedia.org/wiki/Millvina_Dean
             https://www.encyclopedia-titanica.org/titanic-survivor/eva-georgetta-dean.html  
             
             Centrar titulos e imagenes:  
             https://stackoverflow.com/questions/70932538/how-to-center-the-title-and-an-image-in-streamlit  
             
             Emojis:  
             https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/  
             
             GIF code:  
             https://github.com/streamlit/streamlit/issues/1566  
             
             Cabinas y localizaciones (Anna y los Cardeza):  
             https://www.encyclopedia-titanica.org/cabins.html  
             https://www.encyclopedia-titanica.org/titanic-survivor/annie-moore-ward.html  
             
             Pie chart plotly/steamlit:  
             https://stackoverflow.com/questions/74778743/how-to-display-data-across-by-row-in-pie-chart-in-plotly-streamlit  
             
             Reemplazando valores nulos (media, moda y mediana):  
             https://vitalflux.com/pandas-impute-missing-values-mean-median-mode/#:~:text=Mean%20imputation%20is%20often%20used,to%20outliers%20than%20the%20mean.  
             
             Color en el texto:  
             https://medium.com/codefile/streamlit-text-gets-colourful-d92c21ab8cf6  
             
             df.info() en streamlit code:  
             https://discuss.streamlit.io/t/direct-the-output-of-df-info-to-web-page/14894/2  
             
             Certificados de embarque:  
             https://www.encyclopedia-titanica.org/titanic-statistics.html  
             
             Tabla de tarifas:  
             https://www.cruisemummy.co.uk/titanic-ticket-prices/
             https://intriper.com/calcularon-cual-seria-el-precio-de-los-boletos-para-viajar-en-el-titanic-hoy-en-dia/  
             
             Cave List:  
             https://www.encyclopedia-titanica.org/cave-list.html  
             
             Ejemplos de gráficas (mapa con folium - error al cargar eliminada esta parte):  
             https://github.com/bravovielisa/graficas_titanic_ejemplos_para_alumnos/blob/main/Titanic_ejemplos_interactiveg.ipynb
             ''')
    
#----------------------------------------------PESTAÑA 5---------------------------------------------------------# 
#--------------------pestañas----------------------------#
