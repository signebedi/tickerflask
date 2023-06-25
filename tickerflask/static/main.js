function plotGraph(graphJSON) {
    Plotly.react('chart', graphJSON, {});
}

$(document).ready(function () {
    $('#get_latest_price_form form').on('submit', function (e) {
        e.preventDefault();
        var symbol = $('#symbol').val();
        var period = $('#period').val();
        var interval = $('#interval').val();
        $.getJSON('/get_latest_price', { symbol: symbol, period: period, interval: interval })
            .done(function (data) {
                $('#latest_price_result').text(JSON.stringify(data));
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                $('#latest_price_result').text("Request failed, check console for details.");
            });
    });

    $('#get_price_spread_form form').on('submit', function (e) {
        e.preventDefault();
        var symbol = $('#symbol_spread').val();
        var period = $('#period_spread').val();
        var interval = $('#interval_spread').val();
        $.getJSON('/get_price_spread_plotly', { symbol: symbol, period: period, interval: interval })
            .done(function (data) {
                var graphJSON = JSON.parse(data.graphJSON);
                plotGraph(graphJSON);
    
                $('#price_spread_result').text(JSON.stringify(data.data));
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                $('#price_spread_result').text("Request failed, check console for details.");
            });
    });
});