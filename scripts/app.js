var app = new Vue
({
    el: '#app',
    data:
    {
        lista: [],
        input: '',
        dbInfo: 'NotClickedYet'
    },
    methods:
    {
        getTest: function (url) 
        {
            console.log("submitting: " + url)
            axios.get(url).then(function (response) {
                console.log(response);
            }).catch(function (error) {
                console.log(error.message);
            });
    
        },

        recallDB: function()
        {
            axios.get('/db/recall').then(function (response) 
            {
                console.log("success! " + response.data + "\n type: " + typeof(response.data))
                this.dbInfo = response.data
            }).catch (function (error) 
            {
                console.log(error)
            })
        }
    }
})