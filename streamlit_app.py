# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f" :cup_with_straw: Costomize your Smoothie")
st.write(
  """Choose the fruit you want and enjoy your own Smoothie.
  """
)

name_of_order = st.text_input("Name on Smoothie")
st.write("The name will be", name_of_order)


cnx= st.connection("snowflake")
session= cnx.get_active_session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)


ingredient_list= st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)

ingredients_string=''

if ingredient_list:
    

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '

    import streamlit as st

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" +ingredients_string+ """', '"""+name_of_order+ """')"""

#Troubleshoot
#st.write(my_insert_stmt) 
#st.stop()

time_to_insert= st.button('submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered!', icon="✅")

