
function create_table(){
    console.log("creating table")

    $.getJSON("/get_list_receipts_data", function (data, status) {
        amount_of_rows = data.length
        for (let it = 0; it < amount_of_rows; it++) {
            let table = document.getElementById("table_receipts")

            let new_row = document.createElement("tr")
            let column0 = document.createElement("td")
            let check_box = document.createElement("input")
            check_box.type="checkbox"
            column0.appendChild(check_box)

            let column1 = document.createElement("td")
            column1.innerHTML = data[it]["receipt_id"]
            let column2 = document.createElement("td")
            column2.innerHTML = data[it]["rut"]
            let column3 = document.createElement("td")
            column3.innerHTML = data[it]["total_amount"]

            new_row.appendChild(column0)
            new_row.appendChild(column1)
            new_row.appendChild(column2)
            new_row.appendChild(column3)

            table.appendChild(new_row)
        }
    })
 }


 function send_checked(){
    let table = document.getElementById("table_receipts")
    children = table.childNodes

    amount_of_rows = children.length
    receipts_to_send = []

    for (let it = 0; it < amount_of_rows - 2; it++) {
      if(children[it+2].childNodes[0].childNodes[0].checked){
        receipts_to_send.push(children[it+2].childNodes[1].innerText)
      }
    }

     $.ajax({
        type: "POST",
        url: "/download_csv",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(receipts_to_send),
        contentType: "text/csv",
        success: function(data){
            var blob=new Blob([data])
            var link=document.createElement('a')
            link.href=window.URL.createObjectURL(blob)
            link.download="rendiciones.csv"
            link.click()
        },
        error: function(errMsg) {
            alert("ERROR")
        }
    });
    console.log(receipts_to_send)

 }


document.addEventListener("DOMContentLoaded", create_table(), false)