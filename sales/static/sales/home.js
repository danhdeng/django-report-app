console.log("hello from home.js")

const reportbtn=document.getElementById("report-btn")
const img=document.getElementById("img")
const modalBody=document.getElementById("modal-body")
const reportName=document.getElementById("id_name")
const reportRemarks=document.getElementById("id_remarks")
const csrftoken=document.getElementsByName("csrfmiddlewaretoken")[0].value
const reportForm=document.getElementById("report-form")


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
        formData.append('name', reportName)
        formData.append('remarks', reportRemarks)
        formData.append('image', img.src)

        $.ajax({
            type:'POST',
            url : '/reports/save/',
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: formData,
            success: (response)=>(console.log(response)),
            error: (error)=>(console.log(error)),
            processData:false,
            contentType:false
        })
    })
})
