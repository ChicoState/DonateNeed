/*var getPhoto = new Vue(
{
    el: '#get-photo',
    delimiters: ['[[', ']]'],
    data: 
    {
      planetList: []
    },
  
    created: function() 
    {
      this.fetchPlanetList();
      this.timer = setInterval(this.fetchPlanetList, 10000);
    },
    methods: 
    {
        fetchPlanetList: function() 
        {
            axios
            .get('planets/')
            .then(response => (this.planetList = response.data.planets))
    
            console.log("I got the planets!");
            this.seen=false
            this.unseen=true
        },
        cancelAutoUpdate: function() 
        { 
            clearInterval(this.timer) 
        }
    },
    beforeDestroy() 
    {
        clearInterval(this.timer)
    }
})
*/

var add_show_donations = new Vue
(
    {
        el: "#add-show-donations",
        delimiters: ['[[', ']]'],
        data:
        {
            donations: [],
            donation_size: 0
        },

        created: function()
        {
            this.fetchDonations();
        },
        methods:
        {
            makeRequest: function(event)
            {
                this.donation_size = this.donation_size + 1;
                console.log("donation list size: " + this.donation_size);
            },
            submitDonations: function({commit}, payload) 
            {
                console.log("Sending over data.");

                axios
                  .post('/fetch_donation/', payload)
                  .then(response => {this.donations = response.data.donations}); 
            },
            fetchDonations: function()
            {
                axios
                    .get('/fetch_donation/')
                    .then(response => (this.donations = response.data.donations));

                console.log(this.donations);
            }
        }   
    }
)

