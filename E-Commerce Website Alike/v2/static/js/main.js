/*  ---------------------------------------------------
Template Name: Ashion
Description: Ashion ecommerce template
Author: Colorib
Author URI: https://colorlib.com/
Version: 1.0
Created: Colorib
---------------------------------------------------------  */

'use strict';


/*-------------------
	Add Items to Cart
--------------------- */
function add_to_cart(item_id) {
    var quantity = $('.pro-qty[data-item-id="' + item_id + '"]').find('input').val();  // Getting item ID from data attribute

    if (typeof item_id !== 'undefined') {
        // Send the AJAX request to the Flask route
        $.ajax({
            url: '/add_to_cart/' + item_id,
            type: 'POST',
            data: {quantity: quantity},
            success: function (response) {
                if(response.status === 'success') {
                    console.log('Item added to cart: ', response);
                    updateStockLabel(item_id, quantity);
                    showNotification('Item added to cart successfully!', 'success');
                } else {
                    console.log(response.error, 'error');
                    showNotification(response.error, 'error');
                }
            },
            error: function (error) {
                console.log('Error adding item to cart:', error);
                showNotification('Some Error occured, please try again later.');
            }
        });
    } else {
        console.log('Error: Item_id is undefined!');
    }
};


/*-------------------
    Instantly Update Stock
--------------------- */
function updateStockLabel(item_id, quantity) {
    $(document).ready(function() {
        if (document.getElementById('productDetailsPage')) {
            var stockElement = $('.items-left[data-item-id="' + item_id + '"]');
            var currentStockText = stockElement.text();  // e.g., "[10 left!]"
            var matches = currentStockText.match(/\d+/);  // to find digits

            if (matches) {
                var currentStock = parseInt(matches[0], 10);
                var newStock = currentStock - quantity;
                stockElement.text('[' + newStock + ' left!]');  // Update the stock label on the page

                // If newStock is 0, refresh the page after 3 seconds
                if (newStock === 0) {
                    setTimeout(function() {
                        location.reload();
                    }, 1500);
                }

            } else {
                console.log('Could not find stock number in the element\'s text.');
            }
        };
    });
};


    /*-------------------
		Error Display
	--------------------- */
var modal;

function showNotification(message) {
    document.getElementById('notificationMessage').innerText = message;
    modal.style.display = 'block';

    setTimeout(function() {
        modal.style.display = 'none';
    }, 2500);
};

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('productDetailsPage')) {
        modal = document.getElementById('notificationModal');
        var span = document.getElementsByClassName('close')[0];

        if (span) {
            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
              modal.style.display = 'none';
            };
        } else {
            console.log('The close button was not found. Did you change the html identifier?');
        }
    }
});

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
};


(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(50).fadeOut("slow");

        /*------------------
            Product filter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.property__gallery').length > 0) {
            var containerEl = document.querySelector('.property__gallery');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $(document).ready(function() {
        $('.set-bg').each(function() {
            var bg = $(this).data('setbg');
//            console.log(bg);
            $(this).css('background-image', 'url(' + bg + ')');
        });
    });

    //Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay, .offcanvas__close").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".header__menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Accordin Active
    --------------------*/
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev().addClass('active');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev().removeClass('active');
    });

    /*--------------------------
        Banner Slider
    ----------------------------*/
    $(".banner__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*--------------------------
        Product Details Slider
    ----------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop: false,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<i class='arrow_carrot-left'></i>","<i class='arrow_carrot-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
        mouseDrag: false,
        startPosition: 'URLHash'
    }).on('changed.owl.carousel', function(event) {
        var indexNum = event.item.index + 1;
        product_thumbs(indexNum);
    });

    function product_thumbs (num) {
        var thumbs = document.querySelectorAll('.product__thumb a');
        thumbs.forEach(function (e) {
            e.classList.remove("active");
            if(e.hash.split("-")[1] == num) {
                e.classList.add("active");
            }
        })
    }


    /*------------------
		Magnific
    --------------------*/
    $('.image-popup').magnificPopup({
        type: 'image'
    });


    $(".nice-scroll").niceScroll({
        cursorborder:"",
        cursorcolor:"#dddddd",
        boxzoom:false,
        cursorwidth: 5,
        background: 'rgba(0, 0, 0, 0.2)',
        cursorborderradius:50,
        horizrailenabled: false
    });

    /*------------------
        CountDown
    --------------------*/
    // For demo preview start
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    if(mm == 12) {
        mm = '01';
        yyyy = yyyy + 1;
    } else {
        mm = parseInt(mm) + 1;
        mm = String(mm).padStart(2, '0');
    }
    var timerdate = mm + '/' + dd + '/' + yyyy;
    // For demo preview end


    // Uncomment below and use your date //

    /* var timerdate = "2020/12/30" */

	$("#countdown-time").countdown(timerdate, function(event) {
        $(this).html(event.strftime("<div class='countdown__item'><span>%D</span> <p>Day</p> </div>" + "<div class='countdown__item'><span>%H</span> <p>Hour</p> </div>" + "<div class='countdown__item'><span>%M</span> <p>Min</p> </div>" + "<div class='countdown__item'><span>%S</span> <p>Sec</p> </div>"));
    });

    /*-------------------
		Range Slider
	--------------------- */
	var rangeSlider = $(".price-range"),
    minamount = $("#minamount"),
    maxamount = $("#maxamount"),
    minPrice = rangeSlider.data('min'),
    maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
    range: true,
    min: minPrice,
    max: maxPrice,
    values: [minPrice, maxPrice],
    slide: function (event, ui) {
        minamount.val('$' + ui.values[0]);
        maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*------------------
		Single Product
	--------------------*/
	$('.product__thumb .pt').on('click', function(){
		var imgurl = $(this).data('imgbigurl');
		var bigImg = $('.product__big__img').attr('src');
		if(imgurl != bigImg) {
			$('.product__big__img').attr({src: imgurl});
		}
    });

    /*-------------------
		CSRF token for AJAX
	--------------------- */
    // Get the CSRF token from the meta tag
    var csrf_token = $('meta[name="csrf-token"]').attr('content');

    // Set up AJAX to include the CSRF token in the header
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
	$(document).ready(function() {
        var proQty = $('.pro-qty');
        proQty.prepend('<span class="dec qtybtn">-</span>');
        proQty.append('<span class="inc qtybtn">+</span>');
        proQty.on('click', '.qtybtn', function () {
            var $button = $(this);
            var oldValue = $button.parent().find('input').val();
            var newVal = 0;
            if ($button.hasClass('inc')) {
                newVal = parseFloat(oldValue) + 1;
            } else {
                // Don't allow decrementing below zero
                if (oldValue > 0) {
                    newVal = parseFloat(oldValue) - 1;
                }
            }
            $button.parent().find('input').val(newVal);
        });
    });

    /*-------------------
		Radio Btn
	--------------------- */
    $(".size__btn label").on('click', function () {
        $(".size__btn label").removeClass('active');
        $(this).addClass('active');
    });

})(jQuery);
