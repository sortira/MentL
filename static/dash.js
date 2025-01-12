var swiper = new Swiper('.product-slider', {
        spaceBetween: 30,
        effect: 'fade',
        // initialSlide: 2,
        loop: false,
        navigation: {
            nextEl: '.next',
            prevEl: '.prev'
        },
        // mousewheel: {
        //     // invert: false
        // },
        on: {
            init: function(){
                var index = this.activeIndex;

                var target = $('.product-slider__item').eq(index).data('target');

                console.log(target);

                $('.product-img__item').removeClass('active');
                $('.product-img__item#'+ target).addClass('active');
            }
        }
    });

    swiper.on('slideChange', function () {
        var index = this.activeIndex;

        var target = $('.product-slider__item').eq(index).data('target');

        console.log(target);

        $('.product-img__item').removeClass('active');
        $('.product-img__item#'+ target).addClass('active');

        if(swiper.isEnd) {
            $('.prev').removeClass('disabled');
            $('.next').addClass('disabled');
        } else {
            $('.next').removeClass('disabled');
        }

        if(swiper.isBeginning) {
            $('.prev').addClass('disabled');
        } else {
            $('.prev').removeClass('disabled');
        }
    });

    $(".js-fav").on("click", function() {
        $(this).find('.heart').toggleClass("is-active");
    });


    async function submit_sleep()
    {
        const sleep_hours = document.getElementById("sleep_hours").value;
        const sleep_date = document.getElementById("sleep_date").value;

        await fetch('/sleep',
            {
                method:"POST",
                body: JSON.stringify({
                    hours: sleep_hours,
                    date: sleep_date,
                  }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                  }
            });
        location.reload();
    }

    async function submit_exercise()
    {
        const exer_hours = document.getElementById("exercise_hours").value;
        const exer_date = document.getElementById("exercise_date").value;

        await fetch('/physical_activity',
            {
                method:"POST",
                body: JSON.stringify({
                    hours: exer_hours,
                    date: exer_date,
                  }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                  }
            });
        location.reload();
    }

    async function submit_food()
    {
        const food_cal = document.getElementById("food_calories").value;
        const food_date = document.getElementById("food_date").value;

        await fetch('/food',
            {
                method:"POST",
                body: JSON.stringify({
                    calories: food_cal,
                    date: food_date,
                  }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                  }
            });
        location.reload();
    }