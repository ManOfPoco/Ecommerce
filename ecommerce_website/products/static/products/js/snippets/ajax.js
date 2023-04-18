// ajax add item to the wishlist request
export function wishlistAjax(href='http://127.0.0.1:8000/category/grocery/chocolate-and-candy/') {
    $('.wishlist-item-add-form').off().on('submit', function (e) {
        let form = $(this);
        $.ajax({
            type: "POST",
            url: href,
            data: form.serialize() + `&wishlist_item_add=True`,
            success: function (response) {
                if (response.success) {
                    form.find('.modal-messages').html("<div class='alert alert-success my-3' id='success-message'>Product was successfully added to the wishlist</div>")
                } else {
                    form.find('.modal-messages').html("<div class='alert alert-danger my-3' id='error-message'>Product is already exists in this list</div>")
                }
            },
            error: function (response) {
                form.find('.modal-messages').html('<div class="invalid-feedback alert alert-danger d-block">Something went wrong</div>')
            }
        });
        return false;
    });
}