(function () {
    'use strict';
    var isMobile = {
        Android: function () {
            return navigator.userAgent.match(/Android/i);
        }
        , BlackBerry: function () {
            return navigator.userAgent.match(/BlackBerry/i);
        }
        , iOS: function () {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        }
        , Opera: function () {
            return navigator.userAgent.match(/Opera Mini/i);
        }
        , Windows: function () {
            return navigator.userAgent.match(/IEMobile/i);
        }
        , any: function () {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };
    // Preloader
    $(window).load(function() {
    $('.preloader').fadeOut("slow");
    });
    // Animations
    var contentWayPoint = function () {
        var i = 0;
        $('.animate-box').waypoint(function (direction) {
            if (direction === 'down' && !$(this.element).hasClass('animated')) {
                i++;
                $(this.element).addClass('item-animate');
                setTimeout(function () {
                    $('body .animate-box.item-animate').each(function (k) {
                        var el = $(this);
                        setTimeout(function () {
                            var effect = el.data('animate-effect');
                            if (effect === 'fadeIn') {
                                el.addClass('fadeIn animated');
                            }
                            else if (effect === 'fadeInLeft') {
                                el.addClass('fadeInLeft animated');
                            }
                            else if (effect === 'fadeInRight') {
                                el.addClass('fadeInRight animated');
                            }
                            else {
                                el.addClass('fadeInUp animated');
                            }
                            el.removeClass('item-animate');
                        }, k * 200, 'easeInOutExpo');
                    });
                }, 100);
            }
        }, {
            offset: '85%'
        });
    };
    // Burger Menu 
    var burgerMenu = function () {
        $('.js-oliven-nav-toggle').on('click', function (event) {
            event.preventDefault();
            var $this = $(this);
            if ($('body').hasClass('offcanvas')) {
                $this.removeClass('active');
                $('body').removeClass('offcanvas');
            }
            else {
                $this.addClass('active');
                $('body').addClass('offcanvas');
            }
        });
    };
    // Click outside of offcanvass
    var mobileMenuOutsideClick = function () {
        $(document).click(function (e) {
            var container = $("#oliven-aside, .js-oliven-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($('body').hasClass('offcanvas')) {
                    $('body').removeClass('offcanvas');
                    $('.js-oliven-nav-toggle').removeClass('active');
                }
            }
        });
        $(window).scroll(function () {
            if ($('body').hasClass('offcanvas')) {
                $('body').removeClass('offcanvas');
                $('.js-oliven-nav-toggle').removeClass('active');
            }
        });
    };
    // Document on load.
    $(function () {
        contentWayPoint();
        burgerMenu();
        mobileMenuOutsideClick();
    });
    // Sections background image from data background
    var pageSection = $(".bg-img, section");
    pageSection.each(function (indx) {
        if ($(this).attr("data-background")) {
            $(this).css("background-image", "url(" + $(this).data("background") + ")");
        }
    });
    // Friends owlCarousel
    $('.friends .owl-carousel').owlCarousel({
        loop: true
        , margin: 30
        , mouseDrag: true
        , autoplay: false
        , dots: true
        , responsiveClass: true
        , responsive: {
            0: {
                items: 1
            , }
            , 600: {
                items: 2
            }
            , 1000: {
                items: 2
            }
        }
    });
    // When & Where owlCarousel
    $('.whenwhere .owl-carousel').owlCarousel({
        loop: true
        , margin: 30
        , mouseDrag: false
        , autoplay: false
        , dots: true
        , responsiveClass: true
        , responsive: {
            0: {
                items: 1
            , }
            , 600: {
                items: 1
            }
            , 1000: {
                items: 2
            }
        }
    });

    // Accomodations owlCarousel
    $('.accomodations .owl-carousel').owlCarousel({
        loop: true
        , margin: 30
        , mouseDrag: false
        , autoplay: false
        , dots: true
        , responsiveClass: true
        , responsive: {
            0: {
                items: 1
            , }
            , 600: {
                items: 1
            }
            , 1000: {
                items: 4
            }
        }
    });

    // Gift Registry owlCarousel
    $('.gift .owl-carousel').owlCarousel({
        loop: true
        , margin: 30
        , mouseDrag: true
        , autoplay: true
        , dots: false
        , responsiveClass: true
        , responsive: {
            0: {
                margin: 10
                , items: 2
            }
            , 600: {
                items: 3
            }
            , 1000: {
                items: 4
            }
        }
    });
    // Smooth Scrolling
    $('a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });
    // Gallery 
    $(window).on("load", function () {
    var e = $(".gallery-filter")
        , a = $("#gallery-filter");
    e.isotope({
        filter: "*"
        , layoutMode: "masonry"
        , animationOptions: {
            duration: 750
            , easing: "linear"
        }
    }), a.find("a").on("click", function () {
        var o = $(this).attr("data-filter");
        return a.find("a").removeClass("active"), $(this).addClass("active"), e.isotope({
            filter: o
            , animationOptions: {
                animationDuration: 750
                , easing: "linear"
                , queue: !1
            }
        }), !1
    })
});
    // Magnific Popup
    $(".img-zoom").magnificPopup({
    type: "image"
    , closeOnContentClick: !0
    , mainClass: "mfp-fade"
    , gallery: {
        enabled: !0
        , navigateByImgClick: !0
        , preload: [0, 1]
    }
});
}());

// Countdown wedding
  (function () {
  const second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24;
  let birthday = "Nov 4, 2022 17:00:00",
      countDown = new Date(birthday).getTime(),
      x = setInterval(function() {    
        let now = new Date().getTime(),
            distance = countDown - now;

        document.getElementById("days").innerText = Math.floor(distance / (day)),
          document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
          document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
          document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);

        //do something later when date is reached
        if (distance < 0) {
          let headline = document.getElementById("headline"),
              countdown = document.getElementById("countdown"),
              content = document.getElementById("content");

          headline.innerText = "It's our wedding!";
          countdown.style.display = "none";
          content.style.display = "block";

          clearInterval(x);
        }
        //seconds
      }, 0)
  }());

// Show/Hide parts of RSVP form using JQuery
$("#rsvp-main-selection").change(function() {
    if ($(this).val() == "yes") {
        $('#rsvp-num-guests-section').show();
        $('#rsvp-num-guests').attr('required', '');
        $('#rsvp-num-guests').attr('data-error', 'This field is required.');

        $('#primary-email-section').show();
        $('#primary-email').attr('required', '');
        $('#primary-email').attr('data-error', 'This field is required.');

        $('#secondary-email-section').show();
        $('#rsvp-beachday-selection-section').show();
        $('#rsvp-weddingevedinner-selection-section').show();
        $('#rsvp-postweddingbrunch-selection-section').show();
        $('#dietary-restrictions-section').show();
        $('#flights-section').show();
        $('#hotels-section').show();
        $('#message-section').show();


    } else if ($(this).val() == "no") {
        $('#rsvp-num-guests-section').hide();
        $('#rsvp-num-guests').removeAttr('required');
        $('#rsvp-num-guests').removeAttr('data-error');

        $('#primary-email-section').hide();
        $('#primary-email').removeAttr('required');
        $('#primary-email').removeAttr('data-error');

        $('#secondary-email-section').hide();
        $('#rsvp-beachday-selection-section').hide();
        $('#rsvp-weddingevedinner-selection-section').hide();
        $('#rsvp-postweddingbrunch-selection-section').hide();
        $('#dietary-restrictions-section').hide();
        $('#flights-section').hide();
        $('#hotels-section').hide();

        $('#message-section').show();

    } else {

        $('#rsvp-num-guests-section').hide();
        $('#rsvp-num-guests').removeAttr('required');
        $('#rsvp-num-guests').removeAttr('data-error');

        $('#primary-email-section').hide();
        $('#primary-email').removeAttr('required');
        $('#primary-email').removeAttr('data-error');

        $('#secondary-email-section').hide();
        $('#rsvp-beachday-selection-section').hide();
        $('#rsvp-weddingevedinner-selection-section').hide();
        $('#rsvp-postweddingbrunch-selection-section').hide();
        $('#dietary-restrictions-section').hide();
        $('#flights-section').hide();
        $('#hotels-section').hide();
        $('#message-section').hide();
    }
  });

$("#rsvp-main-selection").trigger("change");

// Submit form info
function submitRsvp() {

    let guest_name = document.querySelector('#rsvp-input-name').value;
    let attending_wedding = document.querySelector('#rsvp-main-selection').value;

	if (guest_name != "") {

		console.log("Guest Name: ", guest_name)

        if (attending_wedding == "yes") {
            console.log(guest_name, " is attending the wedding.")

            fetch('/submitRsvp', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					'guest_name': guest_name,
                    'attending': "yes",
                    'rsvp_num_guests': document.querySelector('#rsvp-num-guests').value,
                    'primary_email': document.querySelector('#primary-email').value,
                    'secondary_email': document.querySelector('#secondary-email').value,
                    'rsvp_beachday': document.querySelector('#rsvp-beachday-selection').value,
                    'rsvp_weddingevedinner': document.querySelector('#rsvp-weddingevedinner-selection').value,
                    'rsvp_postweddingbrunch': document.querySelector('#rsvp-postweddingbrunch-selection').value,
                    'dietary_restrictions': document.querySelector('#dietary-restrictions').value,
                    'flights': document.querySelector('#flights').value,
                    'hotels': document.querySelector('#hotels').value,
                    'message': document.querySelector('#message').value,
				})
			})
			.then((response) => response.json())
			.then((jsonResponse) => {
				console.log('Fetch success:', jsonResponse);

                if (jsonResponse['Status'] == 'OK') {
                    $('#rsvp-form-section').hide();
                    $('#post-rsvp-submit-section').show();
                }
                else {
                    $('#rsvp-form-section').hide();
                    $('#post-rsvp-submit-section-error').show();
                }
			});

        }

        else if (attending_wedding == "no") {
            console.log(guest_name, " is NOT attending the wedding.")

            fetch('/submitRsvp', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					'guest_name': guest_name,
                    'attending': "no",
                    'rsvp_num_guests': 0,
                    'message': document.querySelector('#message').value,
				})
			})
			.then((response) => response.json())
			.then((jsonResponse) => {
				console.log('Fetch success:', jsonResponse);

                if (jsonResponse['Status'] == 'OK') {
                    $('#rsvp-form-section').hide();
                    $('#post-rsvp-submit-section').show();
                }
                else {
                    $('#rsvp-form-section').hide();
                    $('#post-rsvp-submit-section-error').show();
                }
			});
        }


	}
}

// Autocomplete
// https://www.w3schools.com/howto/howto_js_autocomplete.asp
function autocomplete(inp) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/

    /* User change: possible autocompleted values retrieved dynamically through a fetch */
    fetch('/getNameRecords', {
        method: 'GET',
        headers: {}
    })
    .then((response) => response.json())
    .then((jsonResponse) => {

        var arr = jsonResponse // The array of names

        var currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function(e) {
            var a, b, i, val = this.value;
            /*close any already open lists of autocompleted values*/
            closeAllLists();
            if (!val) { return false;}
            currentFocus = -1;
            /*create a DIV element that will contain the items (values):*/
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            this.parentNode.appendChild(a);
            /*for each item in the array...*/
            for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            /* User change: check if the test field value matches any substring  */
            if (arr[i].toUpperCase().includes(val.toUpperCase())) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                /* User change: matching letters are the substring  */
                idx = arr[i].toUpperCase().indexOf(val.toUpperCase())
                b.innerHTML += arr[i].substring(0, idx);
                b.innerHTML += "<strong>" + arr[i].substring(idx, idx+val.length) + "</strong>";
                b.innerHTML += arr[i].substring(idx+val.length, arr[i].length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                    b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
            }
        });
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
            } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
            } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
            }
        });
        function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
        }
        function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
        }
        function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
            x[i].parentNode.removeChild(x[i]);
        }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
    }); 
} 