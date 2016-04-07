$(document).ready(function () {
    $(".select-multiple").each(function() {
        var $this = $(this);
        $this.select2({
            placeholder: $this.attr('placeholder'),
            allowClear: true
        });
    });

    var startDate = moment().subtract(10, 'days');
    var endDate = moment();
    var $daterange = $('input[name="daterange"]');
    if ($daterange.val()) {
        var val = $daterange.val().split(' - ');
        var valStartDate = moment(val[0], "YYYY-MM-DD");
        if (valStartDate.isValid()) {
            startDate = valStartDate;
        }
        var valEndDate = moment(val[1], "YYYY-MM-DD");
        if (valEndDate.isValid()) {
            endDate = valEndDate;
        }
    }

    $daterange.daterangepicker({
        startDate: startDate,
        endDate: endDate,
        autoUpdateInput: true,
        locale: {
            format: 'YYYY-MM-DD'
        }
    });
    $daterange.on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });
    $daterange.trigger('apply.daterangepicker', [$daterange.data('daterangepicker')]);

    $(".range_time24").each(function() {
        var range_from = 0,
            range_to = 24*60 - 1;
        var range = $(this).val().split(';');

        if (!isNaN(parseInt(range[0])))
            range_from = parseInt(range[0]);
        if (!isNaN(parseInt(range[1])))
            range_to = parseInt(range[1]);

        $(this).ionRangeSlider({
            type: "double",
            min: 0,
            max: 24*60 - 1,
            from: range_from,
            to: range_to,
            grid: true,
            force_edges: true,
            prettify: function (num) {
                var pad = "00";
                var start = (Math.floor(num/60)).toString(),
                    end = (num % 60).toString();
                return  pad.substring(0, pad.length - start.length) + start + ":" + pad.substring(0, pad.length - end.length) + end;
            }
        });
    });

    var categorical_colors_10 = [
        '#1f77b4',
        '#ff7f0e',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf',
    ];
});

