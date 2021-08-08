const csrftoken=document.getElementsByName("csrfmiddlewaretoken")[0].value;
const alertbox=document.getElementById("alert-box")
console.log(alertbox)
Dropzone.autoDiscover=false;

const fileUpladDropzone=new Dropzone('#fileupload-dropzone', {
    url: '/reports/upload/',
    init: function() {
        this.on('sening', function(file, xhr, formData){
            console.log('sending file');
            formData.append('csrfmiddlewaretoken', csrftoken);
        }),
        this.on('success', function(file, response){
            const ex=response.ex;
            if (ex){
                handlealert('danger','the file already exists.')
            }else{
                handlealert('success','the file had been uploaded.')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptFiles: '.csv',

})