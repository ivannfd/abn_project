function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const lower_indices = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']

function get_conjunct_symbols(atomics_count) {
    const symbols = [];
    for (let i = 1; i < 2 ** atomics_count; i++) {
        let newSymbol = "";
        i.toString(2).split("").reverse().forEach((bit, index) => {
            if (bit === "1") {
                newSymbol = `x${lower_indices[index + 1]}${newSymbol}`
            }
        })
        symbols.push(newSymbol)
    }
       return symbols.map(symbol => `p(${symbol})`)
}

function get_atomic_symbols(atomics_count) {
    symbols = []
    for (let i = 1; i <= atomics_count; i++) {
        symbols.push(`x${lower_indices[i]}`)
    }
    return symbols
}





function check(el) {
    removeResult()

    var a = document.getElementById('nu').value;

    var place = document.getElementById("place")

    if (!document.getElementById("p1")) {

        var elem = document.createElement("p");

        elem.innerHTML = '<b>Вероятностные оценки конъюнктов'
        elem.style.width = '400px'
        elem.style.color = 'black'
        elem.style.margin = '10px 120px'
        elem.id = 'p1'

        place.appendChild(elem);
    }

    var myForm = document.getElementById("checker")
    if (myForm) {
        while (myForm.firstChild) {
            myForm.removeChild(myForm.lastChild);
        }
    } else {
        myForm = document.createElement('form');
        myForm.method = 'post';
        myForm.style.border = '3px solid #ccc';
        myForm.style.margin = '55px 100px';
        myForm.style.padding = '5px';
        myForm.style.background = '#b3e5fc';
        myForm.style.textAlign = 'right';
        myForm.style.width = '380px';
        myForm.id = 'checker'

        myForm.action = "/api/abn_response";

        var inputElem = document.createElement('input');
        inputElem.type = 'hidden';
        inputElem.name = 'csrfmiddlewaretoken';
        inputElem.value = getCookie('csrftoken');
        myForm.appendChild(inputElem);
        place.appendChild(myForm);
    }

     A12=get_conjunct_symbols(a);
     B12=get_atomic_symbols(a);


    for (var i = 1; i < Math.pow(2, a); i++) {

        var elem1 = document.createElement("p");
         //elem1.innerHTML = 'коньюнкт  ' + i;
          elem1.innerHTML=A12[i-1];

        elem1.style.width = '400px'
        elem1.style.margin = '-4px -300px'
        elem1.style.position = 'relative'
        elem1.style.top = '5px'
        myForm.appendChild(elem1);


        var myInput = document.createElement('input');
        myInput.name = 'q';
        myInput.size = 15;
        myInput.placeholder = 'Вероятность'
        myInput.style.margin = '-3px 20px'
        myInput.style.position = 'relative'
        myInput.style.top = '-10px'
        myInput.id = 'conjunct_input_' + i


        myForm.appendChild(myInput);
    }


    var elem2 = document.createElement("p");
    elem2.innerHTML = ' <strong> Введите 1, если утвержение под этим номером истинно, 0 если ложно, - если нет информации'
    elem2.style.width = '400px'
    elem2.style.color = 'black'
    elem2.style.margin = '10px -55px'
    myForm.appendChild(elem2);


    for (var i = 1; i <= a; i++) {

        var elem3 = document.createElement("p");
        //elem3.innerHTML = 'утверждение ' + (i - 1);
        elem3.innerHTML=B12[i-1]
        elem3.style.width = '400px'
        elem3.style.margin = '-5px -300px'
        elem3.style.position = 'relative'
        elem3.style.top = '5px'
        elem3.style.right = '12px'

        myForm.appendChild(elem3);


        var myInput = document.createElement('input');
        myInput.name = 'q';
        myInput.size = 15;
        myInput.placeholder = 'Сведения'
        myInput.style.position = 'relative'
        myInput.style.top = '-10px'
        myInput.style.left = '-20px'
        myInput.id = 'evidence_' + i
        myForm.appendChild(myInput)

    }


    var btn = document.getElementById("btn1")
    if (btn) {
        while (btn.firstChild) {
            btn.removeChild(btn.lastChild);
        }
    } else {
        var elem4 = document.createElement("p");
        myForm.appendChild(elem4);

        btn = document.createElement('input');
        btn.id = 'btn1'
        btn.type = "submit"
        btn.value = 'Получить решение!'
        btn.style.position = 'relative'
        btn.style.top = '-10px'
        btn.style.left = '-20px'
    }
    myForm.appendChild(btn)

    myForm.addEventListener("submit", function (event) {
        event.preventDefault()
        const a = document.getElementById('nu').value;

        let conjuncts_data = [];
        for (let i = 1; i < Math.pow(2, a); i++) {
            conjuncts_data.push(document.getElementById('conjunct_input_' + i).value)
        }
        let evidence_data = []

        for (var i = 1; i <= a; i++) {
            evidence_data.push(document.getElementById('evidence_' + i).value)
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';

        axios
            .post("/api/abn_response", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    conjuncts_data: conjuncts_data,
                    evidence_data: evidence_data,
                    conjuncts_count: a
                }
            })
            .then(response => {
                add_result(response.data['conjuncts_data'])
                // console.log("Это ответ от сервера: " + JSON.stringify(response.data))
            })
            .catch(error => console.log(error));
    });

    return false;
}

function removeResult() {
    const resultContainer = document.getElementById('result');
    if (resultContainer) {
        while (resultContainer.firstChild) {
            resultContainer.removeChild(resultContainer.lastChild);
        }
    }
}

function add_result(result) {
    const resultContainer = document.getElementById('result');
    removeResult()

       var myForm2 = document.createElement('form');
       myForm2.style.border = '3px solid #00FF7F';
       myForm2.style.margin = '55px 100px';
       myForm2.style.padding = '5px';
       myForm2.style.background = '#dcedc8';
       myForm2.style.textAlign = 'right';
       myForm2.style.width = '225px';
       myForm2.style.position = 'fixed'
       myForm2.style.top ='130px'
       myForm2.style.left='600px'
       resultContainer.appendChild(myForm2)





       var resulText = document.createElement("p");
       resulText.innerHTML = ' <strong> Результат:';
       resulText.style.position='relative'
       resulText.style.left='-75px'
       myForm2.appendChild(resulText)


      result=result.slice(1, result.length)

        result.forEach(function (prob, i, res) {
        var probText = document.createElement("p");
        //probText.innerHTML = `Вероятность конъюнкта №${i}: ${prob[0]}`;
          probText.innerHTML = `${A12[i]}= ${prob[0]}`;

        probText.style.position='relative'
         probText.style.left='-85px'
        myForm2.appendChild(probText)
    })
}
