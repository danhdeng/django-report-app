console.log("hello from home.js")

const reportbtn=document.getElementById("report-btn")
const img=document.getElementById("img")
const modalBody=document.getElementById("modal-body")
const reportName=document.getElementById("id_name")
const reportRemarks=document.getElementById("id_remarks")
const csrftoken=document.getElementsByName("csrfmiddlewaretoken")[0].value
const reportForm=document.getElementById("report-form")
const alertbox=document.getElementById("alert-box")
console.log(alertbox)

const handlealert =(type, msg)=>{
    alertbox.innerHTML=`<div class="alert alert-${type}}" role="alert">
        ${msg}
  </div>`
}


console.log(reportForm)
console.log(reportRemarks)

if(img){
    reportbtn.classList.remove("not-visible")
}

reportbtn.addEventListener('click',()=>{
    console.log("report button click")
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)

    reportForm.addEventListener('submit', e=>{
        console.log("save button click")
        e.preventDefault()
        const formData=new FormData()
        formData.append('csrfmiddlewaretoken', csrftoken)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type:'POST',
            url : '/reports/save/',
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: formData,
            success: (response)=>{
                    console.log(response)
                    handlealert("success", "report created")
                },
            error: (error)=>{
                console.log(error)
                handlealert("danger", "oops... something went wrong")
            },
            processData:false,
            contentType:false
        })
    })
})
