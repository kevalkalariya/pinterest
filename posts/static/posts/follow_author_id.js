$(document).ready(function(){
    $("#follow_author_id").click(function(){
        var author_id = $('input[name="pin_author_id"]').val()
        data ={'author_id':author_id}
        $.ajax({
            type : "POST",
            url : '/author_follow_id/',
            data : JSON.stringify(data),
             success:function(response){
                console.log(msg)
             }
        })
    })
})