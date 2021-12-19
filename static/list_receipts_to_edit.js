function create_table(){
    console.log("creating table")

    $.getJSON("/get_list_receipts_data", function (data, status) {
        amount_of_rows = data.length
        for (let it = 0; it < amount_of_rows; it++) {
            let table = document.getElementById("table_receipts")

            let new_row = document.createElement("tr")

            let column0 = document.createElement("td")
            let a_url = document.createElement("a")
            a_url.href="/edit_receipt/" +data[it]["receipt_id"]
            let button = document.createElement("button")
            button.innerText="edit"

            a_url.appendChild(button)
            column0.appendChild(a_url)

            let colum_delete = document.createElement("td")
            let a_url2 = document.createElement("a")
            a_url2.href="/delete_receipt/" +data[it]["receipt_id"]
            let button2 = document.createElement("button")
            button2.innerText="delete"

            a_url2.appendChild(button2)
            colum_delete.appendChild(a_url2)

            let column1 = document.createElement("td")
            column1.innerHTML = data[it]["receipt_id"]
            let column2 = document.createElement("td")
            column2.innerHTML = data[it]["rut"]
            let column3 = document.createElement("td")
            column3.innerHTML = data[it]["total_amount"]

            new_row.appendChild(column0)
            new_row.appendChild(colum_delete)
            new_row.appendChild(column1)
            new_row.appendChild(column2)
            new_row.appendChild(column3)

            table.appendChild(new_row)
        }
    })
 }


 document.addEventListener("DOMContentLoaded", create_table(), false)