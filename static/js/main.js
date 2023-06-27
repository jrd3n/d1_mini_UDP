// import 'chartjs-adapter-moment';


var socket = io.connect('http://localhost:5000');
var last_time = 0;



function requestData() {
    socket.emit('request_data', last_time);
}

let ctx = document.getElementById('myChart').getContext('2d');
let chart = new Chart(ctx, {
    type: 'scatter',
    data: {
        labels: [],  // Initially empty
        datasets: [{
            label: [],
            data: [],  // Initially empty
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
        }]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                },
                
                // ticks: {
                //     source: 'labels'
                // }
            },
            y: {
                // Configure the y-axis as needed
            }
        }
    }

});

socket.on('data_response', function(json_data) {
    // Parse the outer JSON
    let parsedOuterData = JSON.parse(json_data.data);
    
    // Extract timestamp
    last_time = parsedOuterData.timestamp;
    console.log(last_time);  // Inspect the timestamp in the console
    
    // Parse the inner JSON to get the data
    let parsedData = JSON.parse(parsedOuterData.data);
    // console.log(parsedData);  // Inspect the data in the consol

    for (let IP_ADDRESS of parsedData) {
        let IP_ADDRESS_NUMBER = IP_ADDRESS.ip_address;
    
        // Map event_times and raw_values into their respective objects
        let newPoints = IP_ADDRESS.data.map(entry => ({x: new Date(entry.event_time), y: entry.Raw_value}));
        let eventTimes = IP_ADDRESS.data.map(entry => new Date(entry.event_time));
    
        console.log(newPoints);  // This line will log the newPoints array to the console
    
        // Find the dataset for this IP address
        let dataset = chart.data.datasets.find(ds => ds.label === IP_ADDRESS_NUMBER);
    
        if (dataset) {
            // If the dataset exists, append new data to it
            dataset.data.push(...newPoints);
        } else {
            // If the dataset doesn't exist, create a new one
            dataset = {
                label: IP_ADDRESS_NUMBER,
                data: newPoints,
                borderColor: 'rgba(0, 123, 255, 0.5)',
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                fill: false,
                spanGaps: true,
                borderWidth: 2, // Specify the width of the line
                showLine: true,
                animation: false,

            };
            chart.data.datasets.push(dataset);
        }

        chart.data.labels.push(...eventTimes);
    }
    

    


    

    // If the labels array is empty, populate it with eventTimes from the first dataset
    if (chart.data.labels.length === 0 && chart.data.datasets.length > 0) {
        chart.data.labels = parsedData[0].data.map(entry => new Date(entry.event_time));
    }

    // Redraw the chart
    chart.update();
});


// Request data on connection and every 2 seconds afterwards
socket.on('connect', requestData);
setInterval(requestData, 150);