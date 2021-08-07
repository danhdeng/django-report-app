const csrftoken=document.getElementsByName("csrfmiddlewaretoken")[0].value;
console.log(csrftoken);

Dropzone.autoDiscover=false;

const fileUpladDropzone=new Dropzone('#fileupload-dropzone', {
    url: '/reports/upload/',
    init: function() {
        this.on('sening', function(file, xhr, formData){
            console.log('sending file');
            formData.append('csrfmiddlewaretoken', csrftoken);
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptFiles: '.csv',

});