import streamlit as st
import pandas as pd 
from db_funcs import *
from PIL import Image
import plotly.express as px 

def color_df(val):
	if val == "Done":
		color = "green"
	elif val == "Doing":
		color = "orange"
	else:
		color = "red"

	return f'background-color: {color}'

st.set_page_config(
    page_title="Note Creation App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

top_image = Image.open('static/7049.png')
bottom_image = Image.open('static/103-1036487_laptop-png.png')
main_image = Image.open('static/main_banner.png')

st.image(main_image,use_column_width='always')
st.title("📄 Note Creation App 🗣")

st.sidebar.image(top_image,use_column_width='auto')
choice = st.sidebar.selectbox("Menu", ["Create Note ✅","Update Note 👨‍💻","Delete Note ❌", "View Notes' Status 👨‍💻"])
st.sidebar.image(bottom_image,use_column_width='auto')
create_table()

if choice == "Create Note ✅":
	st.subheader("Add Item")
	col1,col2 = st.columns(2)

	with col1:
		task = st.text_area("Notes")

	with col2:
		task_status = st.selectbox("Status",["ToDo","Doing","Done"])
		task_due_date = st.date_input("Due Date")
		tags = st.text_input("Tags (comma-separated)")

	if st.button("Add Note"):
		add_data(task,task_status,task_due_date,tags)
		st.success("Added Note \"{}\" ✅".format(task))
		st.balloons()

elif choice == "Update Note 👨‍💻":
	st.subheader("Edit Items")
	with st.expander("Current Data"):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Note","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	list_of_tasks = [i[0] for i in view_all_task_names()]
	selected_task = st.selectbox("Note",list_of_tasks)
	task_result = get_task(selected_task)

	if task_result:
		task = task_result[0][0]
		task_status = task_result[0][1]
		task_due_date = task_result[0][2]

		col1,col2 = st.columns(2)

		with col1:
			new_task = st.text_area("Note",task)

		with col2:
			new_task_status = st.selectbox(task_status,["To Do","Doing","Done"])
			new_task_due_date = st.date_input(task_due_date)
            

		if st.button("Update Note 👨‍💻"):
			edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date, new_tags)
			st.success("Updated Note \"{}\" ✅".format(task,new_task))

		with st.expander("View Updated Data 💫"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Note","Status","Date"])
			st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

elif choice == "Delete Note ❌":
	st.subheader("Delete")
	with st.expander("View Data"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Note","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	unique_list = [i[0] for i in view_all_task_names()]
	delete_by_task_name =  st.selectbox("Select Note",unique_list)
	if st.button("Delete ❌"):
		delete_data(delete_by_task_name)
		st.warning("Deleted Note \"{}\" ✅".format(delete_by_task_name))

	with st.expander("View Updated Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Note","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

else:
	with st.expander("View All 📝"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Note","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	with st.expander("Note Status 📝"):
		task_df = clean_df['Status'].value_counts().reset_index()
		task_df.columns = ['Status', 'Count']  # Cambiar el nombre de las columnas
		st.dataframe(task_df)
		p1 = px.pie(task_df, names='Status', values='Count', color='Status',
                    color_discrete_map={'ToDo': 'red', 'Done': 'green', 'Doing': 'orange'})
		st.plotly_chart(p1, use_container_width=True)

st.markdown("<br><hr><center>Made for Ensolvers with ❤️ by <a href='mailto:ferreyralorenzo2@gmail.com?subject=Note Creation WebApp!&body=Please specify the issue you are facing with the app.'><strong>Lorenzo</strong></a></center><hr>", unsafe_allow_html=True)
