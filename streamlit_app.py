# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark import session

from snowflake.snowpark import session
    

#session = session.builder.configs(session).create()

from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custome smoothie!
  """
)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on tour smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session

#session = get_active_session()
my_dataframe = session().table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()



ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    ,max_selections= 5
)

if ingredients_list:
     st.write (ingredients_list)
     st.text (ingredients_list)
    
     ingredients_string= ''

for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

    
    st.subheader(fruit_chosen + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen )
    sf_df =st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


  #  st.write (ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

st.write(my_insert_stmt)
#st.stop

#if ingredients_string:
 #   session().sql(my_insert_stmt).collect()
  #  st.success('Your Smoothie is ordered!', icon="✅")

#OU
time_to_insert = st.button('Submit order')
if time_to_insert:
    session().sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#NEW SECTION

#import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df =st.DATAFRAME(data = smoothiefroot_response.json(), use_container_width=True)
