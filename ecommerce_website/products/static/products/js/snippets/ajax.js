// ajax add item to the wishlist request
export function wishlistAjax(href = 'http://127.0.0.1:8000/wishlist/wishlist-item-add/') {
    $('.wishlist-item-add-form').off().on('submit', function (e) {
        let form = $(this);
        $.ajax({
            type: "POST",
            url: href,
            data: form.serialize(),
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

export function moveToCartAjax(href = 'http://127.0.0.1:8000/cart/move-to-cart/') {
    $('.move-to-cart').on('submit', function (e) {
        let form = $(this);
        let product_id = form.find('#data-input').data('product')
        let quantity = $("#quanitity option:selected").val();

        if ($('#quantity').data('quantity') == 0) {
            let id = 'toast-' + new Date().getTime();
            $('.toast-container').append(`
                <div id="${id}" class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="d-flex">
                        <div class="toast-body">
                            Current Item is out of stock!
                        </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                </div>
            `)
            $('.toast#' + id).toast('show');
            return false;
        } else if (quantity == undefined) {
            quantity = 1;
        }

        $.ajax({
            type: "POST",
            url: href,
            data: form.serialize() + `&product_id=${product_id}` + `&quantity=${quantity}`,
            success: function (response) {
                let id = 'toast-' + new Date().getTime();
                if (response.success && response.status === 'Added successfully') {
                    $('.toast-container').append(`
                        <div id="${id}" class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                            <div class="d-flex">
                                <div class="toast-body">
                                    Item added to your cart!
                                </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        </div>
                    `)
                    $('.toast#' + id).toast('show');
                    let count = parseInt($('#cart-items-count').text());
                    $('#cart-items-count').text(count + 1);
                } else if (response.success === false && response.status === 'Object already exists in your cart') {
                    $('.toast-container').append(`
                        <div id="${id}" class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                            <div class="d-flex">
                                <div class="toast-body">
                                    ${response.status}
                                </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        </div>
                    `)
                    $('.toast#' + id).toast('show');
                } else {
                    $('.toast-container').append(`
                    <div id="${id}" class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body">
                                Sorry! Something went wrong!
                            </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                `)
                    $('.toast#' + id).toast('show');
                }
            },
            error: function (response) {
                console.log(response.success);
            }
        });
        return false;
    });
}

