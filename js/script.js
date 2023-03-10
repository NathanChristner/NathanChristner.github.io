const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)

        if (entry.isIntersecting) {

            entry.target.classList.add('show');

        } else {
            entry.target.classList.remove('show');

        }



    });



});

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

// i got this code from this video and adapted it for my website https://www.youtube.com/watch?v=T33NN_pPeNI&ab_channel=BeyondFireship -Nathan