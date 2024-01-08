console.log("Sanity check!");



fetch("/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);
var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// Create an instance of the Stripe object with your publishable API key


        var checkoutButton = document.getElementById("checkout-button");

        checkoutButton.addEventListener("click", function () {
            var address = {
                email: document.getElementById('email').value,
                line1: document.getElementById('address_line1').value,
                city: document.getElementById('address_city').value,
                state: document.getElementById('address_state').value,
                postal_code: document.getElementById('address_postal_code').value,
                country: document.getElementById('address_country').value,
            };


            fetch("/preview-cart/", {
                method: "POST",
                headers: { 'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({address: address}),

            })
                .then(function(response) {

                    return response.json();

                })
                .then(function(responseJson) {
                })


                .then(function () {
                    window.location.href = "/preview-cart/";
                })


                .then(function (result) {
                    // If redirectToCheckout fails due to a browser or network
                    // error, you should display the localized error message to your
                    // customer using error.message.
                    if (result.error) {
                        alert(result.error.message);

                    }

                })

                .catch(function (error) {
                    console.error("Error:", error);
                    // window.location.href = "/error/";
                });
        })
    },);


fetch("/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);
        var checkoutForm = document.getElementById("payment-form");
        const options = {
            clientSecret: checkoutForm.attributes.item(1).nodeValue,
            // Fully customizable with appearance API.
            appearance: {/*...*/},
        };
        console.log(options);
// window.alert(options);

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in a previous step
        const elements = stripe.elements(options);

// Create and mount the Payment Element
        const paymentElement = elements.create('payment');
        paymentElement.mount('#payment-element');


        const form = document.getElementById('payment-form');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const {error} = await stripe.confirmPayment({
                //`Elements` instance that was used to create the Payment Element
                elements,
                confirmParams: {
                    return_url: 'http://0.0.0.0:8000/paymentstatus/',
                },
            });

            if (error) {
                // This point will only be reached if there is an immediate error when
                // confirming the payment. Show error to your customer (for example, payment
                // details incomplete)
                const messageContainer = document.querySelector('#error-message');
                messageContainer.textContent = error.message;
            } else {
                // Your customer will be redirected to your `return_url`. For some payment
                // methods like iDEAL, your customer will be redirected to an intermediate
                // site first to authorize the payment, then redirected to the `return_url`.
            }
        });
    })
