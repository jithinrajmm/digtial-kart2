
let active_inactive = [...document.getElementsByClassName('active_inactive')]

active_inactive.forEach(element=>{
        element.addEventListener('click',function(){
        id=element.dataset.id
        const activate_button = document.getElementById(`active-${id}`)
        $.ajax({
            type:"PUT",
            url: "active_inactive/",
            dataType: "json",
            data:JSON.stringify({'id': id,}),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrftoken,  // don't forget to include the 'getCookie' function
              },
            success:function(response) {
                if (response.user_active_value){
                    activate_button.classList.remove('btn-danger')
                    activate_button.classList.add('btn-success')
                    activate_button.innerText = 'Active'

                }
                else{
                    activate_button.classList.remove('btn-success')
                    activate_button.classList.add('btn-danger')
                    activate_button.innerText = 'Deactive'
                }
                
        
            },
            error:function(error){
                console.log(error)
                console.log('this is error block')
            }
        })

    })
})


const getCookie =(name)=> {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');