function pedidoStatus() {
    let statusPedido = document.querySelectorAll('#status')
    let cardProduto = document.querySelectorAll('#pedido')
    let statusPedidoTxt = document.querySelectorAll('#status')

    for(let i = 0; i < statusPedido.length; i++){
        if(statusPedidoTxt[i].text == 'Pedido pronto') {
            cardProduto[i].style.backgroundColor = '#10642c'
        } if(statusPedidoTxt[i].text == 'Pedido cancelado') {
            cardProduto[i].style.backgroundColor = '#613737'
        }
    }
}

function nonePedido() {
    let displayVar
    
    if (displayVar == 2) {
        displayVar.styles.display = 'none'
    } 
}