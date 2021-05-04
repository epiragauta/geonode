/**
 * @file Create Study Case wizard step
 * validations & interactions
 * @version 1.0
 */
var urlParams = (function(url) {
    var result = new Object();
    var params = window.location.search.slice(1).split('&');
    for (var i = 0; i < params.length; i++) {
        idx = params[i].indexOf('=');
        if (idx > 0) {
            result[params[i].substring(0, idx)] = params[i].substring(idx + 1);
        }
    }
    return result;
})(window.location.href);

var mxLanguage = urlParams['lang'];
var map;
var basinId;
var mapDelimit;
var snapMarker;
var snapMarkerMapDelimit;
var catchmentPoly;
var catchmentPolyDelimit;
var editablepolygon;
var validPolygon;
var isFile;
var delimitationFileType;
var xmlGraph;
var waterExtractionData = {};
var waterExtractionValue;
const delimitationFileEnum = {
    GEOJSON: 'geojson',
    SHP: 'shapefile'
}
const interpolationType = {
    LINEAR: 'LINEAR',
    POTENTIAL: 'POTENTIAL',
    EXPONENTIAL: 'EXPONENTIAL',
    LOGISTICS: 'LOGISTICS'
}

var id_study_case = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);

var intakes = [];
var ptaps = [];

var mapLoader;
$(document).ready(function() {
    $('#autoAdjustHeightF').css("height", "auto");
    $('#cityLabel').text(localStorage.city);
    calculate_Personnel();
    calculate_Platform();
    loadIntakes()
    loadPtaps()
    loadNBS()

    $('#custom').click(function() {
        if ($('#ptap_table').find('tbody > tr').length > 0) {
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!'
            }).then((result) => {
                if (result.isConfirmed) {
                    $("#panel-custom").removeClass("panel-hide");
                    $("#panel-ptap").addClass("panel-hide");
                    $('#autoAdjustHeightF').css("height", "auto");
                    $("#panel-cost").removeClass("panel-hide");
                    $("#ptap_table tbody tr").empty();
                    $('#ptap-required').text("");
                    $('#custom-required').text("*");
                } else {
                    $("input[name=type][value='1']").prop('checked', true);
                }
            })
        } else {
            $("#panel-custom").removeClass("panel-hide");
            $("#panel-ptap").addClass("panel-hide");
            $('#autoAdjustHeightF').css("height", "auto");
            $("#panel-cost").removeClass("panel-hide");
            $('#ptap-required').text("");
            $('#custom-required').text("*");
        }
    });

    $('#ptap').click(function() {
        $("#panel-ptap").removeClass("panel-hide");
        $("#panel-custom").removeClass("panel-hide");
        $("#panel-cost").addClass("panel-hide");
        $('#autoAdjustHeightF').css("height", "auto");
        $('#ptap-required').text("*");
        $('#custom-required').text("");
    });

    $('#btn-full').click(function() {
        if ($("#full-table").hasClass("panel-hide")) {
            $("#full-table").removeClass("panel-hide");
            $("#full-table").find("input").each(function() {
                var $this = $(this).val('');
            });
            $('#autoAdjustHeightF').css("height", "auto");
            $('#column_investment').text("Percentage");
        } else {
            $("#full-table").addClass("panel-hide");
        }
    });

    $('#btn-investment').click(function() {
        if ($("#full-table").hasClass("panel-hide")) {
            $("#full-table").removeClass("panel-hide");
            $('#autoAdjustHeightF').css("height", "auto");
            $('#column_investment').text("Investment");
            $("#full-table").find("input").each(function() {
                var $this = $(this).val('');
            });
        } else {
            $("#full-table").addClass("panel-hide");
        }
    });


    $('#btn-advanced_option').click(function() {
        if ($("#biophysical-panel").hasClass("panel-hide")) {
            $("#biophysical-panel").removeClass("panel-hide");
            $("#biophysical-panel").empty();
            loadBiophysicals();
        } else {
            $("#biophysical-panel").empty();
            $("#biophysical-panel").addClass("panel-hide");
        }
    });


    $('#full').click(function() {
        $("#panel-full").removeClass("panel-hide");
        $("#panel-investment").addClass("panel-hide");
        $("#full-table").addClass("panel-hide");
        $('#autoAdjustHeightF').css("height", "auto");
        $('#column_investment').text("Percentage");
        $("#full-table").find("input").each(function() {
            var $this = $(this).val('');
        });
    });

    $('#investment').click(function() {
        $("#panel-investment").removeClass("panel-hide");
        $("#panel-full").addClass("panel-hide");
        $("#full-table").addClass("panel-hide");
        $('#autoAdjustHeightF').css("height", "auto");
        $('#column_investment').text("Investment");
        $("#full-table").find("input").each(function() {
            var $this = $(this).val('');
        });
    });
    $('#add_wi').click(function() {
        text = $("#select_custom option:selected").text();
        value = $("#select_custom option:selected").val();

        $('#select_custom option:selected').remove();
        var action = "<td><a class='btn btn-danger'><span class='glyphicon glyphicon-trash' aria-hidden='true'></span></a></td>";
        $.get("../../study_cases/intakebyid/" + value, function(data) {
            $.each(data, function(index, intake) {
                var name = "<td>" + intake.name + "</td>";
                var name_source = "<td>" + intake.water_source_name + "</td>";
                var markup = "<tr id='custom-" + value + "'>" + name + name_source + action + "</tr>";
                $("#custom_table").find('tbody').append(markup);
            });

            $('#autoAdjustHeightF').css("height", "auto");
        });

    });

    $('#add_ptap').click(function() {
        text = $("#select_ptap option:selected").text();
        value = $("#select_ptap option:selected").val();
        $('#select_ptap option:selected').remove();
        var action = "<td><a class='btn btn-danger'><span class='glyphicon glyphicon-trash' aria-hidden='true'></span></a></td>";
        $.get("../../study_cases/ptapbyid/" + value, function(data) {
            $.each(data, function(index, ptap) {
                var name = "<td>" + ptap.plant_name + "</td>";
                var description = "<td>" + ptap.plant_description + "</td>";
                var markup = "<tr id='ptap-" + value + "'>" + name + description + action + "</tr>";
                $("#ptap_table").find('tbody').append(markup);
            });
        });
        $.get("../../study_cases/intakebyptap/" + value, function(data) {
            $.each(data, function(index, intake) {
                id = intake.csinfra_elementsystem__intake__id
                $("#select_custom option").each(function(i) {
                    if (id == $(this).val()) {
                        $(this).remove();
                    }
                });
                $("#custom-" + id).remove();
            });
        });
        $('#autoAdjustHeightF').css("height", "auto");
    });


    $('#step1NextBtn').click(function() {
        intakes = [];
        ptaps = [];
        valid_ptaps = true;
        valid_intakes = true;
        $('#custom_table').find('tbody > tr').each(function(index, tr) {
            id = tr.id.replace('custom-', '')
            intakes.push(id)
        });
        if (intakes.length <= 0) {
            valid_intakes = false
        }
        var type = $("input[name='type']:checked").val();
        if (type == "1") {
            $('#ptap_table').find('tbody > tr').each(function(index, tr) {
                id = tr.id.replace('ptap-', '')
                ptaps.push(id)
            });
            if (ptaps.length <= 0) {
                valid_ptaps = false;
            } else {
                valid_intakes = true
            }
        }
        if (($('#name').val() != '' && $('#description').val() != '' && valid_intakes && valid_ptaps)) {
            $.post("../../study_cases/save/", {
                name: $('#name').val(),
                id_study_case: id_study_case,
                description: $('#description').val(),
                intakes: intakes,
                ptaps: ptaps,
                city: localStorage.city,
                country: localStorage.country,
                type: type
            }, function(data) {
                id_study_case = data.id_study_case;
                if (id_study_case == '') {
                    Swal.fire({
                        icon: 'warning',
                        title: `Study Case exist`,
                        text: `please change the name`
                    });
                    return;
                } else {
                    $('#smartwizard').smartWizard("next");
                    $('#autoAdjustHeightF').css("height", "auto");
                }

            }, "json");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please full every fields`
            });
            return;
        }
    });

    $("#cb_check").click(function() {
        console.log("si")
        if ($(this).is(":checked")) // "this" refers to the element that fired the event
        {
            $("#cm_form").show();
            $('#autoAdjustHeightF').css("height", "auto");
        } else {
            $("#cm_form").hide();
            $('#autoAdjustHeightF').css("height", "auto");
        }
    })

    $('#step2PreviousBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step2NextBtn').click(function() {
        $.post("../../study_cases/save/", {
            id_study_case: id_study_case,
            carbon_market: $("#cb_check").is(':checked'),
            carbon_market_value: $('#id_cm').val(),
            carbon_market_currency: $("#cm_select option:selected").text()
        }, function(data) {
            $('#smartwizard').smartWizard("next");
            $('#autoAdjustHeightF').css("height", "auto");
        }, "json");

    });

    $('#step3PreviousBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step3NextBtn').click(function() {
        portfolios = [];
        $('#portfolios-ul input:checked').each(function() {
            id = $(this).attr("id").replace('portfolio-', '')
            portfolios.push(id)
        })
        if (portfolios.length > 0) {
            $.post("../../study_cases/save/", {
                id_study_case: id_study_case,
                portfolios: portfolios
            }, function(data) {
                $('#smartwizard').smartWizard("next");
                $('#autoAdjustHeightF').css("height", "auto");
            }, "json");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please check options`
            });
            return;
        }
    });

    $('#step4PreviousBtn').click(function() {
        $("#biophysical-panel").empty();
        $('#smartwizard').smartWizard("prev");
    });

    $('#step4NextBtn').click(function() {
        biophysical = []
        $('#biophysical-panel').find('table').each(function(index, table) {
            id = table.id.split('_').pop()
            bio = {
                intake_id: id
            }
            $('#' + table.id).find('tbody > tr.edit').each(function(index, tr) {
                bio[id] = id = tr.id.split('_').pop();
                $('#' + tr.id).find('td').each(function(index, td) {
                    td_id = td.id
                    if (td_id) {
                        split = td_id.split('_')
                        split.pop();
                        name_td = split.join("_");
                        val = undefined
                        $('#' + td.id).find("input").each(function() {
                            val = $(this).val();
                        });
                        if (!val) {
                            val = $('#' + td.id).text();
                        }
                        bio[name_td] = val;
                    }
                });
                biophysical.push(bio)
            });

        });
        console.log(biophysical)
        $.post("../../study_cases/savebio/", {
            id_study_case: id_study_case,
            biophysicals: '1' + JSON.stringify(biophysical),
            process: "Edit",
        }, function(data) {
            $('#smartwizard').smartWizard("next");
            loadFinancialParameter()
            $('#autoAdjustHeightF').css("height", "auto");
        }, "json");

    });


    $('#step5PreviousBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step5NextBtn').click(function() {
        var valid = true;
        $("#div_financial").find("input").each(function() {
            var $this = $(this);
            if ($this.val().length <= 0) {
                valid = false;
                return false;
            }
        });
        var min = $('#minimum').val()
        var max = $('#maximum').val()
        if ($('#minimum').val() >= $('#maximum').val()) {
            Swal.fire({
                icon: 'warning',
                title: `Minimum value`,
                text: `Please check minimum value`
            });
            valid = false
            return;
        }
        if (($('#discount').val() < $('#minimum').val()) || ($('#discount').val() > $('#maximum').val())) {
            Swal.fire({
                icon: 'warning',
                title: `Discount value`,
                text: `Please check discount`
            });
            valid = false
            return;
        }

        if (valid) {
            $.post("../../study_cases/save/", {
                id_study_case: id_study_case,
                director: $('#director').val(),
                implementation: $('#implementation').val(),
                evaluation: $('#evaluation').val(),
                finance: $('#finance').val(),
                office: $('#office').val(),
                overhead: $('#overhead').val(),
                equipment: $('#equipment').val(),
                discount: $('#discount').val(),
                minimum: $('#minimum').val(),
                minimum: $('#minimum').val(),
                transaction: $('#transaction').val(),
                travel: $('#travel').val(),
                contracts: $('#contracts').val(),
                others: $('#others').val(),
                total_platform: $('#total_platform').val(),
                financial_currency: $("#financial_currency option:selected").text()
            }, function(data) {
                $('#smartwizard').smartWizard("next");
                $('#autoAdjustHeightF').css("height", "auto");
            }, "json");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please check options`
            });
            return;
        }
    });

    $('#step6PreviousBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step6NextBtn').click(function() {
        nbs = [];
        $('#nbs-ul input:checked').each(function() {
            id = $(this).attr("id").replace('nbs-', '')
            nbs.push(id)
        })
        if (nbs.length > 0) {
            $.post("../../study_cases/save/", {
                id_study_case: id_study_case,
                nbs: nbs
            }, function(data) {
                $('#smartwizard').smartWizard("next");
                $('#autoAdjustHeightF').css("height", "auto");
                loadNBSActivities()
            }, "json");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please check options`
            });
            return;
        }
    });

    $('#step7PreviousBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });


    $('#step7EndBtn').click(function() {
        edit = !$("#full-table").hasClass("panel-hide")
        var valid_edit = true;
        var valid_investment = true;
        var valid_period = true;
        nbsactivities = []
        if (edit) {
            var valid_edit = true;
            $("#full-table").find("input").each(function() {
                var $this = $(this);
                if ($this.val().length <= 0) {
                    valid_edit = false;
                    return false;
                }
            });
        }
        if ($('#period_analysis').val() < 10 || $('#period_analysis').val() > 100) {
            Swal.fire({
                icon: 'warning',
                title: `Field problem`,
                text: `Please check period value`
            });
            valid_period = false;
            return
        }
        var type = $("input[name='analysis_type']:checked").val();
        if (type == "2") {
            valid_investment = $('#annual_investment').val() != ''
        }
        if ($('#period_analysis').val() != '' && $('#period_nbs').val() != '' && type && valid_edit && valid_investment && valid_period) {
            $("#full-table").find("input").each(function(index, input) {
                nbsactivity = {}
                input_id = input.id
                if (input_id) {
                    split = input_id.split('-')
                    nbssc_id = split.pop();
                    val = $("#" + input_id).val()
                    nbsactivity['id'] = nbssc_id;
                    nbsactivity['value'] = val;
                    nbsactivities.push(nbsactivity)
                }
            });
            $.post("../../study_cases/save/", {
                id_study_case: id_study_case,
                analysis_type: type,
                period_nbs: $('#period_nbs').val(),
                period_analysis: $('#period_analysis').val(),
                analysis_nbs: $("#analysis_nbs option:selected").val(),
                analysis_currency: $("#analysis_currency option:selected").text(),
                annual_investment: $('#annual_investment').val(),
                rellocated_remainder: $("#rellocated_check").is(':checked'),
                nbsactivities: '1' + JSON.stringify(nbsactivities),
            }, function(data) {
                $('#smartwizard').smartWizard("next");
                $('#autoAdjustHeightF').css("height", "auto");
            }, "json");
            $("#form").submit();
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please check options`
            });
            return;
        }

    });


    $('#custom_table').on('click', 'a', function() {
        var row = $(this).closest("tr")
        var tds = row.find("td");
        intake_name = "";
        $.each(tds, function(i) {
            if (i == 0) {
                intake_name = $(this).text();
            }
        });
        option = intake_name
        id = row.attr("id").replace('custom-', '')
        $("#select_custom").append(new Option(option, id));
        row.remove();

    });

    $('#ptap_table').on('click', 'a', function() {
        var row = $(this).closest("tr")
        var tds = row.find("td");
        ptap_name = "";
        $.each(tds, function(i) {
            if (i == 0) {
                ptap_name = $(this).text();
            }

        });
        option = ptap_name
        id = row.attr("id").replace('ptap-', '')
        $.get("../../study_cases/intakebyptap/" + id, function(data) {
            $.each(data, function(index, intake) {
                id = intake.csinfra_elementsystem__intake__id
                option = intake.csinfra_elementsystem__intake__name
                $("#select_custom").append(new Option(option, id));
            });
        });
        $("#select_ptap").append(new Option(option, id));
        row.remove();

    });

    function loadFinancialParameter() {
        $.get("../../study_cases/parametersbycountry/" + localStorage.country, function(data) {
            $.each(data, function(index, financialParameters) {
                if (!$("#director").val())
                    $("#director").val(financialParameters.Program_Director_USD_YEAR);
                if (!$("#evaluation").val())
                    $("#evaluation").val(financialParameters.Monitoring_and_Evaluation_Manager_USD_YEAR);
                if (!$("#finance").val())
                    $("#finance").val(financialParameters.Finance_Manager_USD_YEAR);
                if (!$("#implementation").val())
                    $("#implementation").val(financialParameters.Implementation_Manager_USD_YEAR);
                if (!$("#office").val())
                    $("#office").val(financialParameters.Office_Costs_USD_YEAR);
                if (!$("#equipment").val())
                    $("#equipment").val(financialParameters.Equipment_Purchased_In_Year_1_USD);
                if (!$("#overhead").val())
                    $("#overhead").val(financialParameters.Overhead_USD_YEAR);
                if (!$("#discount").val())
                    $('#discount').val(financialParameters.drt_discount_rate_medium);
                if (!$("#minimum").val())
                    $('#minimum').val(financialParameters.drt_discount_rate_lower_limit);
                if (!$("#maximum").val())
                    $('#maximum').val(financialParameters.drt_discount_rate_upper_limit);
                if (!$("#transaction").val())
                    $('#transaction').val(financialParameters.Transaction_cost);
                if (!$("#contracts").val())
                    $('#contracts').val(0);
                if (!$("#travel").val())
                    $('#travel').val(0);
                if (!$("#others").val())
                    $('#others').val(0);
                calculate_Personnel();
                calculate_Platform();
            });
        });
    }

    $('#biophysical-panel').on('keyup change', 'table tr input', function() {
        var row = $(this).closest("tr")
        row.addClass("edit");

    });

    $("#director").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });

    $("#evaluation").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });

    $("#finance").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });

    $("#implementation").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });

    $("#office").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });
    $("#travel").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });
    $("#equipment").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });
    $("#overhead").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });
    $("#contracts").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });
    $("#others").keyup(function() {
        calculate_Personnel();
        calculate_Platform();
    });

    function calculate_Personnel() {
        var total = 0.0;
        var total_personnel = $("#total_personnel");
        var director = $("#director").val();
        var evaluation = $("#evaluation").val();
        var finance = $("#finance").val();
        var implementation = $("#implementation").val();
        if (director && !isNaN(director)) {
            total += parseFloat(director)
        }
        if (evaluation && !isNaN(evaluation)) {
            total += parseFloat(evaluation)
        }
        if (finance && !isNaN(finance)) {
            total += parseFloat(finance)
        }
        if (implementation && !isNaN(implementation)) {
            total += parseFloat(implementation)
        }
        total_personnel.val(total)
    }

    function calculate_Platform() {
        var total = 0.0;
        var total_plaform = $("#total_platform");
        var personnel = $("#total_personnel").val();
        var office = $("#office").val();
        var travel = $("#travel").val();
        var equipment = $("#equipment").val();
        var overhead = $("#overhead").val();
        var contracts = $("#contracts").val();
        var others = $("#others").val();

        if (personnel && !isNaN(personnel)) {
            total += parseFloat(personnel)
        }
        if (director && !isNaN(director)) {
            total += parseFloat(director)
        }
        if (office && !isNaN(office)) {
            total += parseFloat(office)
        }
        if (travel && !isNaN(travel)) {
            total += parseFloat(travel)
        }
        if (equipment && !isNaN(equipment)) {
            total += parseFloat(equipment)
        }
        if (contracts && !isNaN(contracts)) {
            total += parseFloat(contracts)
        }
        if (overhead && !isNaN(overhead)) {
            total += parseFloat(overhead)
        }
        if (others && !isNaN(others)) {
            total += parseFloat(others)
        }
        total_plaform.val(total)
    }

    function calculateAnalysisValues(input) {
        var type = $("input[name='analysis_type']:checked").val();
        var total = 100
        if (type == "2") {
            total = $('#annual_investment').val()
        }
        if (total != '') {
            suma = 0.0;
            $("#full-table").find("input").each(function() {
                var $this = $(this);
                if ($this.val().length > 0) {
                    suma += Number($this.val());
                    if (suma > total) {
                        input.val('')
                        Swal.fire({
                            icon: 'warning',
                            title: `greater value`,
                            text: `the sum of values ​​is greater than ` + total
                        });
                    }
                }
            });
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please add annual investment`
            });
            return;
        }
    }


    $('#smartwizard').smartWizard({
        selected: 0,
        theme: 'dots',
        enableURLhash: false,
        autoAdjustHeight: true,
        transition: {
            animation: 'fade', // Effect on navigation, none/fade/slide-horizontal/slide-vertical/slide-swing
        },
        toolbarSettings: {
            toolbarPosition: 'bottom', // both bottom
            toolbarButtonPosition: 'center', // both bottom
        },
        keyboardSettings: {
            keyNavigation: false
        },
        toolbarSettings: {
            showNextButton: false,
            showPreviousButton: false,
        }
    });

    $('#autoAdjustHeightF').css("height", "auto");

    function loadIntakes() {
        var city = localStorage.city
        $.get("../../study_cases/intakebycity/" + city, function(data) {
            if (data.length > 0) {
                $.each(data, function(index, intake) {
                    contains = false
                    $('#custom_table').find('tbody > tr').each(function(index, tr) {
                        id = tr.id.replace('custom-', '')
                        if (id == intake.id) {
                            contains = true
                            return false
                        }
                    });
                    if (!contains) {
                        var name = intake.name;
                        option = name
                        $("#select_custom").append(new Option(option, intake.id));
                    }

                });
                $("#div-customcase").removeClass("panel-hide");
                $('#autoAdjustHeightF').css("height", "auto");
            } else {
                $("#div-emptyintakes").removeClass("panel-hide");
            }

        });
    }

    function loadPtaps() {
        var city = localStorage.city
        $.get("../../study_cases/ptapbycity/" + city, function(data) {
            if (data.length > 0) {
                $.each(data, function(index, ptap) {
                    contains = false
                    $('#ptap_table').find('tbody > tr').each(function(index, tr) {
                        id = tr.id.replace('ptap-', '')
                        if (id == ptap.id) {
                            contains = true
                            return false
                        }
                    });
                    if (!contains) {
                        var name = ptap.plant_name;
                        option = name
                        $("#select_ptap").append(new Option(option, ptap.id));
                    }

                });
                $("#div-ptaps").removeClass("panel-hide");
                $('#autoAdjustHeightF').css("height", "auto");
            } else {
                $("#radio-ptap").addClass("panel-hide");
                $("#div-emptyptaps").removeClass("panel-hide");
            }

        });
    }

    function loadNBS() {
        var country = localStorage.country
        $.post("../../study_cases/nbs/", {
            id_study_case: id_study_case,
            country: country,
            process: "Edit"
        }, function(data) {
            content = ''
            $.each(data, function(index, nbs) {
                var name = nbs.name;
                var id = nbs.id
                var def = nbs.default
                content = '<li class="list-group-item"><div class="custom-control custom-checkbox">'
                if (def) {
                    content += '<input type="checkbox" class="custom-control-input" id="nbs-' + id + '" checked>'
                } else {
                    content += '<input type="checkbox" class="custom-control-input" id="nbs-' + id + '">'
                }
                content += '<label class="custom-control-label" for="nbs-' + id + '"> ' + name + '</label></div></li>'
                $("#nbs-ul").append(content);
            });
            $('#autoAdjustHeightF').css("height", "auto");

        });
    }

    function loadNBSActivities() {
        var country = localStorage.country
        $.post("../../study_cases/nbs/", {
            id_study_case: id_study_case,
            country: country,
            process: "View"
        }, function(data) {
            content = ''
            values = false
            $.each(data, function(index, nbs) {
                var name = nbs.name;
                var id = nbs.id_nbssc
                var def = nbs.default
                var val = nbs.value;
                if (val) {
                    values = true
                }
                if (def) {
                    content += '<tr><td>' + name + '</td>'
                    content += '<td><input class="text-number" type="number" id="nbssc-' + id + '" value="' + val + '"> </td></tr > '
                }
            });
            $("#full-table").find('tbody').append(content);
            $('#full-table tbody tr td input').on('keyup', function(e) {
                calculateAnalysisValues($(this))
            });
            if (values) {
                $("#full-table").removeClass('panel-hide');
            }
            $('#autoAdjustHeightF').css("height", "auto");

        });
    }


    function loadBiophysicals() {
        if (ptaps.length > 0) {
            $.each(ptaps, function(index, id_ptap) {
                $.get("../../study_cases/intakebyptap/" + id_ptap, function(data) {
                    $.each(data, function(index, intake) {
                        loadBiophysical(intake.csinfra_elementsystem__intake__id, intake.csinfra_elementsystem__intake__name)
                    });
                });
            });

        }
        if (intakes.length > 0) {
            $.each(intakes, function(index, id_intake) {
                $.get("../../study_cases/intakebyid/" + id_intake, function(data) {
                    intake = data[0];
                    loadBiophysical(intake.id, intake.name)
                });
            });

        }
    }

    function loadBiophysical(id_intake, name) {
        $.post("../../study_cases/bio/", {
            id_intake: id_intake,
            id_study_case: id_study_case,
        }, function(data) {
            labels = data[0]
            content = '<div class="col-md-12"><legend><label>Intake ' + name + '</span> </label></legend>'
            content += '<table id="bio_table_' + id_intake + '" class="table table-striped table-bordered table-condensed" style="width:100%"><thead><tr class="info">'
            content += '<th scope="col" class="small text-center vat">description</th>'
            content += '<th scope="col" class="small text-center vat">lucode</th>'
            $.each(labels, function(key, v) {
                if (key != 'lucode' && key != 'default' && key != 'lulc_desc' && key != 'description' && key != 'user_id' && key != 'intake_id' && key != 'study_case_id' && key != 'id' && key != 'macro_region' && key != 'kc') {
                    content += '<th scope="col" class="small text-center vat">' + key + '</th>'
                }
            });
            content += '</tr></thead><tbody>'
            $.each(data, function(index, bio) {
                content += '<tr id="id_' + bio.id + '">'
                content += '<td id="description_' + bio.id + '">' + bio.description + '</td>'
                content += '<td id="lucode_' + bio.id + '">' + bio.lucode + '</td>'
                $.each(bio, function(key, v) {
                    if (key != 'lucode' && key != 'default' && key != 'lulc_desc' && key != 'description' && key != 'user_id' && key != 'intake_id' && key != 'study_case_id' && key != 'id' && key != 'macro_region' && key != 'kc') {
                        content += '<td id="' + key + '_' + bio.id + '"><input class="text-number" type="number" value="' + v + '"/></td>'
                    }
                });
                content += '</tr>'
            });
            content += '</tbody></table></div>'
            $("#biophysical-panel").append(content);
            $('#autoAdjustHeightF').css("height", "auto");

        });



        content += '</tbody></table>'
    }


});




window.onbeforeunload = function() {
    return mxResources.get('changesLost');
};