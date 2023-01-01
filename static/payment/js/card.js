// var stripe = Stripe('sk_test_51MJcUwH08zSRRhwiyUS73WwzcRvIQGpL03Gor11hZrdzpzflAsYX7arBlmlG4TdKS4yYyplxWSBBmYeGQI79SABn00ZbIEc0BQ');

// var elem = document.getElementById('submit');
// clientSecret = elem.getAttribute('data-secret');

// var elements = stripe.elements();
// var style = {
//     base: {
//         color: '#000',
//         lineHeight: '2.4',
//         fontSize: '16px',
//     }
// };

// var card = elements.create("card", { style: style });
// card.mount("#card-element");

// card.on('change', function(event) {
//     var displayError = document.getElementById('card-errors')
//     if (event.error) {
//         displayError.textContent = event.error.message;
//         $('#card-errors').addClass('alert alert-info');
//     } else {
//         displayError.textContent = '';
//         $('#card-errors').removeClass('alert alert-info');
//     }
// });

// var form = document.getElementById('payment-form');
// form.addEventListener('submit', function(event) {
//     event.preventDefault();

//     var customerName = document.getElementById("cst-name").value,
//         customerAddress = document.getElementById("cst-address").value,
//         postCode = document.getElementById("cst-postcode").value;

//     stripe.confirmCardPayment(clientSecret, {
//         payment_method: {
//             card: card,
//             billing_details: {
//                 address: {
//                     line1: customerAddress,
//                     line2: customerAddress,
//                 },
//             name: customerName,
//             },
//         }
//     })
// }).then(function(result) {
//     if (result.error) console.log("Error: \n" + result.error.message);
//     else {
//         if (result.paymentIntent.status === 'succeeded') {
//             console.log('Payment Processed');

//             window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
//         }
//     }
// });

var stripe = Stripe('sk_test_51MJcUwH08zSRRhwiyUS73WwzcRvIQGpL03Gor11hZrdzpzflAsYX7arBlmlG4TdKS4yYyplxWSBBmYeGQI79SABn00ZbIEc0BQ');

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();

var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;


  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2
            },
            name: custName
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {},
  });



});