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
            
        },
        methods:
        {
            makeRequest: function(event)
            {
                this.donation_size = this.donation_size + 1;
                this.updateDonation();
                console.log("donation list size: " + this.donation_size);
            },
            updateDonation: function(event)
            {
                var slider = document.getElementById("myRange");
                var output = document.getElementById("demo");
                output.innerHTML = slider.value + " / " + slider.max;
                console.log("Value of Slider: " + slider.value);
            }
        }
    }
)


var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}

