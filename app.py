import streamlit as st
import requests as rq
import pandas as pd

server_loc = st.secrets["server"]
st.title("EXPENSE TRACKER APPLICATION")
opt = st.sidebar.selectbox(
    "Choose Operation",["ADD_EXPENSE","VIEW_EXPENSES","DELETE_EXPENSE","UPDATE_EXPENSE","SEARCH_EXPENSE","SORT_EXPENSES"])
if opt == "ADD_EXPENSE":
    st.header("ADD EXPENSE")
    with st.form("adding"):
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount", step=1)
        category = st.selectbox(
            "Category",[ "Food", "Travel","Shopping","Bills","Entertainment"]
        )
        btn = st.form_submit_button("ADD EXPENSE")
        if btn:
            new_data = {
                "t": title,
                "a": amount,
                "c": category
            }
            res = rq.post(
                f"{server_loc}/add_expense",
                json=new_data
            )
            st.success(res.json()["msg"])


elif opt == "VIEW_EXPENSES":
    st.header("VIEW EXPENSES")
    res = rq.get(f"{server_loc}/view_expenses")
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
elif opt == "DELETE_EXPENSE":
    st.header("DELETE EXPENSE")
    expense_id=st.number_input("Enter Expense id",step=1)
    if st.button("DELETE"):
        res=rq.delete(f"{server_loc}/delete_expense/{expense_id}")
        st.success(res.json()["msg"])
elif opt == "UPDATE_EXPENSE":
    st.header("UPDATE EXPENSE")
    expense_id = st.number_input(
        "Enter Expense ID",
        step=1
    )
    title = st.text_input("New Title")
    amount = st.number_input(
        "New Amount",
        step=1
    )
    category = st.selectbox("New Category",["Food","Travel","Shopping", "Bills","Entertainment"])
    if st.button("UPDATE"):
        update_data = {
            "t": title,
            "a": amount,
            "c": category
        }
        res = rq.put(
            f"{server_loc}/update_expense/{expense_id}",
            json=update_data
        )

        st.success(res.json()["msg"])
elif opt == "SEARCH_EXPENSE":
    st.header("SEARCH EXPENSE")
    category = st.selectbox(
        "Choose Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment"
        ]
    )
    if st.button("SEARCH"):

        res = rq.get(
            f"{server_loc}/search_expense/{category}"
        )

        data = res.json()

        df = pd.DataFrame(data)

        st.dataframe(df)
elif opt == "SORT_EXPENSES":
    st.header("SORT EXPENSES")
    sort_type = st.selectbox(
        "Sort By",
        [
            "high",
            "low"
        ]
    )
    if st.button("SORT"):

        res = rq.get(
            f"{server_loc}/sort_expense/{sort_type}"
        )
        data = res.json()
        df = pd.DataFrame(data)
        st.dataframe(df)


