function vAddPedido(frm) {
    var qtdPedido = document.querySelector('#quantidadeItemPedido')

    if(qtdPedido.value < 1) {
        alert('Quantidade de item inválido, tente novamente!')
        return false
    }
    frm.submit()
}