edge = edge || {};


edge.api = (() => {

    let get = (callback) => {

        edge.ajax('/api/cart/', 'GET', undefined, callback);

    };


    let add = (itemId, callback) => {

        edge.ajax('/api/cart/add/', 'POST', {id: itemId}, callback);

    };


    let update = (cartItem, callback) => {

        edge.ajax('/api/cart/update/', 'POST', {id: cartItem.id, quantity: cartItem.quantity}, callback);

    };


    let remove = (cartItem, callback) => {

        edge.ajax('/api/cart/remove/', 'POST', {id: cartItem.id}, callback);

    };


    let clear = (callback) => {

        edge.ajax('/api/cart/clear/', 'POST', undefined, callback);

    };


    return {
        get,
        add,
        update,
        remove,
        clear
    }

})();
