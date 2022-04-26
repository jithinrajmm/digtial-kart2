var product_view_button = [...document.getElementsByClassName('product_name')]
const modal_close = document.getElementById('modal_close')
// const product_update_forms = [...document.getElementsByClassName('product_update')]
// console.log(product_update_forms)








const pro_name = document.getElementById('id_product_name')
const category = document.getElementById('id_category')
const price = document.getElementById('id_price')
const slug = document.getElementById('id_slug')
const stock = document.getElementById('id_stock')
const description = document.getElementById('id_description')
const image1 = document.getElementById('img1')
const image2 = document.getElementById('img2')
const image3 = document.getElementById('img3')
const image4 = document.getElementById('img4')

// THIS IS THE INPUT TYPE FILE IDS 

const image1_input = document.getElementById('id_image_1')
const image2_input = document.getElementById('id_image_2')
const image3_input = document.getElementById('id_image_3')
const image4_input = document.getElementById('id_image_4')



modal_close.addEventListener('click',function(){
    $("#exampleModal").modal('hide')
})

product_view_button.forEach(Element=>
    {
        Element.addEventListener('click',function(){
            id=Element.dataset.id
            $.ajax({
                url:'testing',
                type: 'GET',
                data:{ 'id': id },
                success:function(response){
                    $("#exampleModal").modal('show')
                    image1.classList.remove('hide')
                    image2.classList.remove('hide')
                    image3.classList.remove('hide')
                    image4.classList.remove('hide')
                    pro_name.value = response.products.name
                    category.selectedIndex = response.products.category_count;
                    slug.value = response.products.slug
                    price.value = response.products.price
                    stock.value = response.products.stock
                    description.value = response.products.description
                    image1.src = response.products.image_1
                    image2.src = response.products.image_2
                    image3.src = response.products.image_3
                    image4.src = response.products.image_4
                    // const product_update_forms = document.getElementById('product_update')
                    

                },
                error: function(errors){
                    console.log(errors)
                }
            })
        })
    })

// // product update 
// product_update_forms.forEach(function(form_update){
//     form_update.addEventListener('submit',(e)=>{
//         const csrf = document.getElementsByName('csrfmiddlewaretoken')
//         e.preventDefault()
//         const formData = new FormData()
//         formData.append('csrfmiddlewaretoken',csrf[0].value)
//         formData.append('product_name',pro_name.value)
//         formData.append('slug',slug.value)
//         formData.append('category',category.value)
//         formData.append('price',price.value)
//         formData.append('stock',stock.value)
//         formData.append('description',description.value)
//         if (image1_input.files[0]){
//             formData.append('image_1',image1_input.files[0])
//             console.log(formData.get('image_1'))
//         }
//         if (image2_input.files[0]){
//             formData.append('image_2',image2_input.files[0])
//             console.log(formData.get('image_2'))
//         }
//         if (image3_input.files[0]){
//             formData.append('image_3',image3_input.files[0])
//             console.log(formData.get('image_3'))
//         }
//         if (image4_input.files[0]){
//             formData.append('image_4',image4_input.files[0])
//             console.log(formData.get('image_4'))
//         }

//         $.ajax({
//             url:'',
//             method:'POST',
//             data: formData,
//             enctype: 'multipart/form-data',
//             processData: false,
//             contentType: false,
//             cache: false, 
//         })
        
        

//     })
// })
 


    // this is for the image 1
$('#id_image_1').change( function(event) {
    var tmppath = URL.createObjectURL(event.target.files[0]);
    $('#img1').removeClass('hide')
    $("#img1").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    
    $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
});

// this is for the image 2
$('#id_image_2').change( function(event) {
    var tmppath = URL.createObjectURL(event.target.files[0]);
    $('#img2').removeClass('hide')
    $("#img2").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    
    $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
});


// this is for the image 3 
$('#id_image_3').change( function(event) {
    var tmppath = URL.createObjectURL(event.target.files[0]);
    $('#img3').removeClass('hide')
    $("#img3").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    
    $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
});


// this is for the image 4
$('#id_image_4').change( function(event) {
    var tmppath = URL.createObjectURL(event.target.files[0]);
    $('#img4').removeClass('hide')
    $("#img4").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    
    $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
});
