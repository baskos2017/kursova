const form = document.querySelector("form")
const password = document.querySelector('input[name="password"]')
const confirmPassword = document.querySelector('input[name="confirm_password"]')
function validation(event){
    event.preventDefault()
    if (password.value == confirmPassword.value){
        form.submit()
        
    } else{
        confirmPassword.style.background = 'red'
    }
}

form.addEventListener('submit', validation)