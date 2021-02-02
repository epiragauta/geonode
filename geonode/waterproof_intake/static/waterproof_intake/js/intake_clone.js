/**
 * @file Create Intake wizard step
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
var copyCoordinates = [];
var editablepolygon;
var validPolygon;
var isFile;
var delimitationFileType;
var xmlGraph;
var waterExtractionData = {};
var waterExtractionValue;
var lyrsPolygons = [];
const delimitationFileEnum = {
    GEOJSON: 'geojson',
    SHP: 'shapefile'
}
const interpMethodInput = $('#typeProcessInterpolation');
const numYearsInput = $('#numberYearsInterpolationValue');
const initialExtraction = $('#initialDataExtractionInterpolationValue');
const finalExtraction = $('#finalDataExtractionInterpolationValue');
const interpolationType = {
    LINEAR: 'LINEAR',
    POTENTIAL: 'POTENTIAL',
    EXPONENTIAL: 'EXPONENTIAL',
    LOGISTICS: 'LOGISTICS'
}

var mapLoader;
$(document).ready(function() {

    $("#intakeWECB").click(function() {
        $('#intakeECTAG tr').remove();
        $('#IntakeTDLE table').remove();
        $('#externalSelect option').remove();
        $('#autoAdjustHeightF').css("height", "auto");
        typeProcessInterpolation = Number($("#typeProcessInterpolation").val());
        numberYearsInterpolationValue = Number($("#numberYearsInterpolationValue").val());
        initialDataExtractionInterpolationValue = parseFloat($("#initialDataExtractionInterpolationValue").val());
        finalDataExtractionInterpolationValue = parseFloat($("#finalDataExtractionInterpolationValue").val());

        // Linear interpolation
        if (typeProcessInterpolation == 1) {
            waterExtractionValue = [];
            waterExtractionData.typeInterpolation = interpolationType.LINEAR;
            m = (finalDataExtractionInterpolationValue - initialDataExtractionInterpolationValue) / (numberYearsInterpolationValue - 0)
            b = (-1 * m * 0) + initialDataExtractionInterpolationValue;

            for (let index = 0; index <= numberYearsInterpolationValue; index++) {
                var yearData = {};
                yearData.year = index + 1;
                yearData.value = ((m * index) + b).toFixed(2);
                waterExtractionValue.push(yearData);
                $('#intakeECTAG').append(`<tr>
                <th class="text-center" scope="row">${index}</th>
                <td class="text-center"><input type="text" class="form-control" value="${((m * index) + b).toFixed(2)}" disabled></td>
              </tr>`);
            }
        }

        // Potencial interpolation
        if (typeProcessInterpolation == 2) {
            waterExtractionValue = [];
            waterExtractionData.typeInterpolation = interpolationType.POTENTIAL;
            m = (Math.log(finalDataExtractionInterpolationValue) - Math.log(initialDataExtractionInterpolationValue)) / ((Math.log(numberYearsInterpolationValue + 1) - Math.log(1)));
            b = Math.exp((-1 * m * Math.log(1)) + Math.log(initialDataExtractionInterpolationValue));

            for (let index = 1; index <= numberYearsInterpolationValue + 1; index++) {
                var yearData = {};
                yearData.year = index;
                yearData.value = (b * (Math.pow(index, m))).toFixed(2);
                waterExtractionValue.push(yearData);
                $('#intakeECTAG').append(`<tr>
                <th class="text-center" scope="row">${index - 1}</th>
                <td class="text-center"><input type="text" class="form-control" value="${(b * (Math.pow(index, m))).toFixed(2)}" disabled></td>
              </tr>`);
            }
        }

        // Exponential interpolation
        if (typeProcessInterpolation == 3) {
            waterExtractionValue = [];
            waterExtractionData.typeInterpolation = interpolationType.EXPONENTIAL;
            m = (Math.log(finalDataExtractionInterpolationValue) - Math.log(initialDataExtractionInterpolationValue)) / (numberYearsInterpolationValue - 0)
            b = Math.exp((-1 * m * 0) + Math.log(initialDataExtractionInterpolationValue));

            for (let index = 0; index <= numberYearsInterpolationValue; index++) {
                var yearData = {};
                yearData.year = index + 1;
                yearData.value = (b * (Math.exp(m * index))).toFixed(2);
                waterExtractionValue.push(yearData);
                $('#intakeECTAG').append(`<tr>
                <th class="text-center" scope="row">${index}</th>
                <td class="text-center"><input type="text" class="form-control" value="${(b * (Math.exp(m * index))).toFixed(2)}" disabled></td>
              </tr>`);
            }

        }

        // Interpolación Logistica
        if (typeProcessInterpolation == 4) {
            waterExtractionValue = [];
            waterExtractionData.typeInterpolation = interpolationType.LOGISTICS;
            r = (-Math.log(0.000000001) / initialDataExtractionInterpolationValue);

            for (let index = 0; index <= numberYearsInterpolationValue; index++) {
                var yearData = {};
                yearData.year = index + 1;
                yearData.value = ((finalDataExtractionInterpolationValue) / (1 + ((finalDataExtractionInterpolationValue / initialDataExtractionInterpolationValue) - 1) * Math.exp(-r * index))).toFixed(2);
                waterExtractionValue.push(yearData);
                $('#intakeECTAG').append(`<tr>
                <th class="text-center" scope="row">${index}</th>
                <td class="text-center"><input type="text" class="form-control" value="${((finalDataExtractionInterpolationValue) / (1 + ((finalDataExtractionInterpolationValue / initialDataExtractionInterpolationValue) - 1) * Math.exp(-r * index))).toFixed(2)}" disabled></td>
              </tr>`);
            }
        }
        externalInput(numberYearsInterpolationValue);
        // Set object data for later persistence
        waterExtractionData.yearCount = numberYearsInterpolationValue;
        waterExtractionData.initialValue = initialDataExtractionInterpolationValue;
        waterExtractionData.finalValue = finalDataExtractionInterpolationValue;
        waterExtractionData.yearValues = waterExtractionValue;
        $('#waterExtraction').val(JSON.stringify(waterExtractionData));

    });
    setInterpolationParams();

    function externalInput(numYear) {
        var rows = "";
        $('#externalSelect').append(`<option value="null" selected>Choose here</option>`);
        for (let p = 0; p < graphData.length; p++) {
            if (graphData[p].external == 'true') {
                $('#externalSelect').append(`
                            <option value="${graphData[p].id}">${graphData[p].id} - External Input</option>
                 `);
                rows = "";
                for (let index = 0; index <= numYear; index++) {
                    rows += (`<tr>
                                <th class="text-center" scope="col" name="year_${graphData[p].id}" year_value="${index + 1}">${index + 1}</th>
                                <td class="text-center" scope="col"><input type="text" class="form-control" name="waterVolume_${index + 1}_${graphData[p].id}"></td>
                                <td class="text-center" scope="col"><input type="text" class="form-control" name="sediment_${index + 1}_${graphData[p].id}"></td>
                                <td class="text-center" scope="col"><input type="text" class="form-control" name="nitrogen_${index + 1}_${graphData[p].id}" ></td>
                                <td class="text-center" scope="col"><input type="text" class="form-control" name="phosphorus_${index + 1}_${graphData[p].id}"></td>
                          </tr>`);
                }
                $('#IntakeTDLE').append(`
                        <table class="table" id="table_${graphData[p].id}" style="display: none">
                            <thead>
                                <tr>
                                    <th class="text-center" scope="col">Year</th>
                                    <th class="text-center" scope="col">Water Volume (m3)</th>
                                    <th class="text-center" scope="col">Sediment (Ton)</th>
                                    <th class="text-center" scope="col">Nitrogen (Kg)</th>
                                    <th class="text-center" scope="col">Phosphorus (Kg)</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>    
                `);
            }

        }


    }
    $('#saveExternalData').click(function() {
        for (let id = 0; id < graphData.length; id++) {
            if (graphData[id].external) {
                graphData[id].externaldata = [];
                $(`th[name=year_${graphData[id].id}]`).each(function() {
                    graphData[id].externaldata.push({
                        "year": $(this).attr('year_value'),
                        "water": $(`input[name="waterVolume_${$(this).attr('year_value')}_${graphData[id].id}"]`).val(),
                        "sediment": $(`input[name="sediment_${$(this).attr('year_value')}_${graphData[id].id}"]`).val(),
                        "nitrogen": $(`input[name="nitrogen_${$(this).attr('year_value')}_${graphData[id].id}"]`).val(),
                        "phosphorus": $(`input[name="phosphorus_${$(this).attr('year_value')}_${graphData[id].id}"]`).val()
                    })
                });
                graphData[id].externaldata = JSON.stringify(graphData[id].externaldata);
            }
        }


        $('#graphElements').val(JSON.stringify(graphData));
    });

    $('#externalSelect').change(function() {
        for (let t = 0; t < graphData.length; t++) {
            if (graphData[t].external == 'true') {
                $(`#table_${graphData[t].id}`).css('display', 'none');
            }
        }
        $(`#table_${$('#externalSelect').val()}`).css('display', 'block');
    });

    $('#smartwizard').smartWizard("next").click(function() {
        $('#autoAdjustHeightF').css("height", "auto");
        mapDelimit.invalidateSize();
        map.invalidateSize();
    });

    $('#intakeNIBYMI').click(function() {
        $('#intakeWEMI div').remove();
        intakeNIYMI = Number($("#intakeNIYMI").val());
        for (let index = 0; index < intakeNIYMI; index++) {
            $('#intakeWEMI').append(`<div class="form-group">
                <label class="col-sm-1 control-label">${index + 1}</label>
                <div class="col-sm-11">
                    <input type="text" class="form-control">
                </div>
            </div>`);
        }
    });
    $('#smartwizard').smartWizard("next").click(function() {
        $('#autoAdjustHeightF').css("height", "auto");
        map.invalidateSize();
    });
    $('#smartwizard').smartWizard({
        selected: 0,
        theme: 'dots',
        enableURLhash: false,
        autoAdjustHeight: true,
        transition: {
            animation: 'slide-horizontal', // Effect on navigation, none/fade/slide-horizontal/slide-vertical/slide-swing
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
    $("#smartwizard").on("showStep", function(e, anchorObject, stepIndex, stepDirection) {
        if (stepIndex == 4) {
            if (catchmentPoly) {
                mapDelimit.invalidateSize();
                mapDelimit.fitBounds(catchmentPoly.getBounds());
            } else {
                mapDelimit.invalidateSize();
                $('#autoAdjustHeightF').css("height", "auto");
            }
            changeFileEvent();
        }
        if (stepIndex == 0) {
            if (catchmentPoly) {
                map.invalidateSize();
                map.fitBounds(catchmentPoly.getBounds());
            } else {
                map.invalidateSize();
                $('#autoAdjustHeightF').css("height", "auto");
            }
        }
    });


    //Validated of steps
    $('#step1NextBtn').click(function() {
        if ($('#id_name').val() != '' && $('#id_description').val() != '' && $('#id_water_source_name').val() != '' && catchmentPoly != undefined) {
            $('#smartwizard').smartWizard("next");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Field empty`,
                text: `Please full every fields`
            });
            return;
        }
    });

    $('#step2PrevBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step2NextBtn').click(function() {
        if (!bandera) {
            $('#smartwizard').smartWizard("stepState", [3], "hide");
            for (const item of graphData) {
                if (item.external != null && item.external != 'false') {

                    $('#smartwizard').smartWizard("stepState", [3], "show");
                }
            }
            $('#smartwizard').smartWizard("next");
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Validate Graph`,
                text: `Please Validate Graph`
            });
            return;
        }
    });

    $('#step3PrevBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step3NextBtn').click(function() {
        $('#IntakeTDLE table').remove();
        $('#externalSelect option').remove();
        $('#externalSelect').append(`<option value="null" selected>Choose here</option>`);
        if ($('#intakeECTAG')[0].childNodes.length > 1) {
            $('#smartwizard').smartWizard("next");
            var tempNum = 0;
            for (let index = 0; index < graphData.length; index++) {
                if (graphData[index].external == "true") {
                    tempNum += 1;
                }
            }
            if (tempNum == intakeExternalInputs.length) {
                loadExternalInput();
            } else {
                $('#IntakeTDLE table').remove();
                $('#IntakeTDLE').empty();
                $('#externalSelect option').remove();
                $('#externalSelect').empty();
            }
        } else {
            Swal.fire({
                icon: 'warning',
                title: `Data analisys empty`,
                text: `Please Generate Data anlisys`
            });
            return;
        }

    });

    function loadExternalInput() {

        for (const extractionData of intakeExternalInputs) {
            $('#externalSelect').append(`
                <option value="${extractionData.xmlId}">${extractionData.xmlId} - External Input</option>
            `);
            rows = "";
            for (let index = 0; index < extractionData.waterExtraction.length; index++) {
                rows += (`<tr>
                        <th class="text-center" scope="col" name="year_${extractionData.waterExtraction[index].year}" year_value="${index + 1}">${index + 1}</th>
                        <td class="text-center" scope="col"><input type="text" value="${extractionData.waterExtraction[index].waterVol}" class="form-control" name="waterVolume__${extractionData.xmlId}"></td>
                        <td class="text-center" scope="col"><input type="text" value="${extractionData.waterExtraction[index].sediment}" class="form-control" name="sediment__${extractionData.xmlId}"></td>
                        <td class="text-center" scope="col"><input type="text" value="${extractionData.waterExtraction[index].nitrogen}" class="form-control" name="nitrogen__${extractionData.xmlId}" ></td>
                        <td class="text-center" scope="col"><input type="text" value="${extractionData.waterExtraction[index].phosphorus}" class="form-control" name="phosphorus__${extractionData.xmlId}"></td>
                  </tr>`);

            }
            $('#IntakeTDLE').append(`
                  <table class="table" id="table_${extractionData.xmlId}" style="display: none;">
                      <thead>
                          <tr>
                              <th class="text-center" scope="col">Year</th>
                              <th class="text-center" scope="col">Water Volume (m3)</th>
                              <th class="text-center" scope="col">Sediment (Ton)</th>
                              <th class="text-center" scope="col">Nitrogen (Kg)</th>
                              <th class="text-center" scope="col">Phosphorus (Kg)</th>
                          </tr>
                      </thead>
                      <tbody>${rows}</tbody>
                  </table>    
          `);
        }

    }

    $('#step4PrevBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    $('#step4NextBtn').click(function() {
        $('#smartwizard').smartWizard("next");
    });

    $('#step5PrevBtn').click(function() {
        $('#smartwizard').smartWizard("prev");
    });

    // Change Option Manual Tab
    $('#btnManualTab').click(function() {
        if ($('#initialDataExtractionInterpolationValue').val() != '' || $('#finalDataExtractionInterpolationValue').val() != '' || $('#numberYearsInterpolationValue').val() != '') {
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: false,
                showDenyButton: true,
                confirmButtonColor: '#d33',
                denyButtonColor: '#3085d6',
                confirmButtonText: 'Yes, change it!',
                denyButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    $('#intakeECTAG tr').remove();
                    $('#IntakeTDLE table').remove();
                    $('#externalSelect option').remove();
                    $('#intakeECTAG').empty();
                    $('#IntakeTDLE').empty();
                    $('#externalSelect').empty();
                    waterExtractionData = [];
                    $('#waterExtraction').val(JSON.stringify(waterExtractionData));
                    $('#initialDataExtractionInterpolationValue').val('');
                    $('#finalDataExtractionInterpolationValue').val('');
                    $('#numberYearsInterpolationValue').val('');
                } else if (result.isDenied) {
                    $('[href="#automatic"]').tab('show');
                }
            })
        }
    });

    // Change Option Automatic with Wizard Tab
    $('#btnAutomaticTab').click(function() {
        if ($('#intakeNIYMI').val() != '') {
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: false,
                showDenyButton: true,
                confirmButtonColor: '#d33',
                denyButtonColor: '#3085d6',
                confirmButtonText: 'Yes, change it!',
                denyButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    $('#intakeWEMI tr').remove();
                    $('#IntakeTDLE table').remove();
                    $('#externalSelect option').remove();
                    $('#intakeWEMI').empty();
                    $('#IntakeTDLE').empty();
                    $('#externalSelect').empty();
                    waterExtractionData = [];
                    $('#waterExtraction').val(JSON.stringify(waterExtractionData));
                    $('#intakeNIYMI').val('');
                } else if (result.isDenied) {
                    $('[href="#manual"]').tab('show');
                }
            })
        }
    });

    map = L.map('map', {}).setView([4.1, -74.1], 5);
    mapDelimit = L.map('mapid', { editable: true }).setView([4.1, -74.1], 5);
    var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    });
    var osmid = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    });
    map.addLayer(osm);
    var images = L.tileLayer("https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}");
    var esriHydroOverlayURL = "https://tiles.arcgis.com/tiles/P3ePLMYs2RVChkJx/arcgis/rest/services/Esri_Hydro_Reference_Overlay/MapServer/tile/{z}/{y}/{x}";
    var hydroLyr = L.tileLayer(esriHydroOverlayURL);
    var baseLayers = {
        OpenStreetMap: osm,
        Images: images,
        /* Grayscale: gray,   */
    };
    var overlays = {
        "Hydro (esri)": hydroLyr,
    };
    var c = new L.Control.Coordinates();
    c.addTo(map);
    L.control.layers(baseLayers, overlays, { position: 'topleft' }).addTo(map);
    mapDelimit.addLayer(osmid);
    intakePolygons.forEach(feature => {
        let poly = feature.polygon;
        let point = feature.point;
        let delimitPolygon = feature.delimitArea;
        if (delimitPolygon.indexOf("SRID") >= 0) {
            delimitPolygon = delimitPolygon.split(";")[1];
        }

        let delimitLayerTransformed = omnivore.wkt.parse(delimitPolygon);
        let delimitLayerKeys = Object.keys(delimitLayerTransformed._layers);
        let keyNameDelimitPol = delimitLayerKeys[0];
        let delimitPolyCoord = delimitLayerTransformed._layers[keyNameDelimitPol].feature.geometry.coordinates[0];
        delimitPolyCoord.forEach(function(geom) {
            var coordinates = [];
            coordinates.push(geom[1]);
            coordinates.push(geom[0]);
            copyCoordinates.push(coordinates);
        })
        let ll = new L.LatLng(feature.point.geometry.coordinates[1], feature.point.geometry.coordinates[0]);
        snapMarker = L.marker(null, {});
        snapMarkerMapDelimit = L.marker(null, {});
        snapMarker.setLatLng(ll);
        snapMarkerMapDelimit.setLatLng(ll);
        snapMarker.addTo(map);
        snapMarkerMapDelimit.addTo(mapDelimit);
        catchmentPoly = L.geoJSON(JSON.parse(feature.polygon)).addTo(map);
        catchmentPolyDelimit = L.geoJSON(JSON.parse(feature.polygon)).addTo(mapDelimit);
        map.fitBounds(catchmentPoly.getBounds());
        editablepolygon = L.polygon(copyCoordinates, { color: 'red' });
        editablepolygon.addTo(mapDelimit);
        var editablePolygonJson = editablepolygon.toGeoJSON();
        var intakePolygonJson = catchmentPoly.toGeoJSON();
        var pointIntakeJson = snapMarker.toGeoJSON();
        basinId = feature.basin;
        $('#intakeAreaPolygon').val(JSON.stringify(intakePolygonJson));
        $('#basinId').val(basinId);
        // Set delimited area geom in hidden input for posterior reading
        $('#delimitArea').val(JSON.stringify(editablePolygonJson));
        $('#pointIntake').val(JSON.stringify(pointIntakeJson));
        $('#isFile').val(JSON.stringify(isFile));
        $('#typeDelimit').val(JSON.stringify(delimitationFileType));
    });

    $("#validateBtn").on("click", function() {
        Swal.fire({
            title: 'Delimitar punto y cuenca',
            text: "El sistema ajustará las coordenadas del punto a la captación más cercana, ¿Desea continuar?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ajustar punto',
            cancelButtonText: 'Cancelar',
        }).then((result) => {
            if (result.isConfirmed) {
                mapLoader = L.control.loader().addTo(map);
                validateCoordinateWithApi();
            }
        })
    });
    $('#btnDelimitArea').on("click", delimitIntakeArea)
    $('#btnValidateArea').on("click", validateIntakeArea)
    if (!mapLoader) {
        mapLoader = L.control.loader().addTo(map);
    }

    mapLoader.hide();

    createEditor(editorUrl);

    var menu1Tab = document.getElementById('mapid');
    var observer2 = new MutationObserver(function() {
        if (menu1Tab.style.display != 'none') {
            mapDelimit.invalidateSize();
        }
    });
    observer2.observe(menu1Tab, { attributes: true });

});
// window.onbeforeunload = function() { return mxResources.get('changesLost'); };

/*Set values for interpolation
parameters*/
function setInterpolationParams() {
    switch (intakeInterpolationParams.type) {
        // LINEAR INTERPOLATION
        case interpolationType.LINEAR:
            // Method interpolation select
            interpMethodInput.val(1);
            // Years number for time series
            numYearsInput.val(intakeInterpolationParams.yearsNum);
            // Initial extraction value
            initialExtraction.val(intakeInterpolationParams.initialExtract);
            // Final extraction value
            finalExtraction.val(intakeInterpolationParams.endingExtract);
            $("#intakeWECB").click();
            break;
            // POTENTIAL INTERPOLATION
        case interpolationType.POTENTIAL:
            interpMethodInput.val(2);
            // Years number for time series
            numYearsInput.val(intakeInterpolationParams.yearsNum);
            // Initial extraction value
            initialExtraction.val(intakeInterpolationParams.initialExtract);
            // Final extraction value
            finalExtraction.val(intakeInterpolationParams.endingExtract);
            $("#intakeWECB").click();
            break;
            // EXPONENTIAL INTERPOLATION
        case interpolationType.EXPONENTIAL:
            interpMethodInput.val(3);
            // Years number for time series
            numYearsInput.val(intakeInterpolationParams.yearsNum);
            // Initial extraction value
            initialExtraction.val(intakeInterpolationParams.initialExtract);
            // Final extraction value
            finalExtraction.val(intakeInterpolationParams.endingExtract);
            $("#intakeWECB").click();
            break;

            // LOGISTICS INTERPLATION
        case interpolationType.LOGISTICS:
            interpMethodInput.val(4);
            // Years number for time series
            numYearsInput.val(intakeInterpolationParams.yearsNum);
            // Initial extraction value
            initialExtraction.val(intakeInterpolationParams.initialExtract);
            // Final extraction value
            finalExtraction.val(intakeInterpolationParams.endingExtract);
            $("#intakeWECB").click();
            break;
    }
}
/** 
 * Delimit manually the intake polygon
 */
function delimitIntakeArea() {
    isFile = false;
    copyCoordinates = [];
    console.log('Delimiting');
    var polygonKeys = Object.keys(catchmentPoly._layers);
    var keyNamePolygon = polygonKeys[0];
    var geometryCoordinates = catchmentPoly._layers[keyNamePolygon].feature.geometry.coordinates[0];
    geometryCoordinates.forEach(function(geom) {
        var coordinates = [];
        coordinates.push(geom[1]);
        coordinates.push(geom[0]);
        copyCoordinates.push(coordinates);
    })
    mapDelimit.removeLayer(editablepolygon);
    editablepolygon = L.polygon(copyCoordinates, { color: 'red' });
    editablepolygon.addTo(mapDelimit)
    editablepolygon.enableEdit();
    editablepolygon.on('dblclick', L.DomEvent.stop).on('dblclick', editablepolygon.toggleEdit);
}

function validateIntakeArea() {
    var editablePolygonJson = editablepolygon.toGeoJSON();
    var intakePolygonJson = catchmentPoly.toGeoJSON();
    var pointIntakeJson = snapMarker.toGeoJSON();
    /** 
     * Get filtered activities by transition id 
     * @param {String} url   activities URL 
     * @param {Object} data  transition id  
     *
     * @return {String} activities in HTML option format
     */
    $.ajax({
        url: '/intake/validateGeometry/',
        type: 'POST',
        data: {
            'editablePolygon': JSON.stringify(editablePolygonJson),
            'intakePolygon': JSON.stringify(intakePolygonJson),
            'isFile': JSON.stringify(isFile),
            'typeDelimit': delimitationFileType
        },
        success: function(result) {
            if (!result.validPolygon) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error de Geometría',
                    text: 'El polígono editado no es válido, por favor intente de nuevo',
                })
            } else if (!result.polygonContains) {
                Swal.fire({
                        icon: 'error',
                        title: 'El polígono debe estar dentro del área de la captación',
                        text: 'El polígono editado no es válido, por favor intente de nuevo',
                    })
                    // Correct geometry
            } else {
                Swal.fire(
                    'Excelente',
                    'El polígono es válido y está dentro de la captación',
                    'success'
                );
                // Set original intake area geom in hidden input for posterior reading
                $('#intakeAreaPolygon').val(JSON.stringify(intakePolygonJson));
                $('#basinId').val(basinId);
                // Set delimited area geom in hidden input for posterior reading
                $('#delimitArea').val(JSON.stringify(editablePolygonJson));
                $('#pointIntake').val(JSON.stringify(pointIntakeJson));
                $('#isFile').val(JSON.stringify(isFile));
                $('#typeDelimit').val(JSON.stringify(delimitationFileType));
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

/** 
 * Validate input file on change
 * @param {HTML} dropdown Dropdown selected element
 */
function changeFileEvent() {
    $('#intakeArea').change(function(evt) {
        var file = evt.currentTarget.files[0];
        var extension = validExtension(file);
        // Validate file's extension
        if (extension.valid) { //Valid
            console.log('Extension valid!');
            isFile = true;
            // Validate file's extension
            if (extension.extension == 'geojson') { //GeoJSON
                var readerGeoJson = new FileReader();
                readerGeoJson.onload = function(evt) {
                    var contents = evt.target.result;
                    try {
                        geojson = JSON.parse(contents);
                        validGeojson = validateGeoJson(geojson);
                        if (validGeojson) {
                            delimitationFileType = delimitationFileEnum.GEOJSON;
                            let polygonStyle = {
                                fillColor: "red",
                                color: "#333333",
                                weight: 0.2,
                                fillOpacity: 0.3
                            };
                            editablepolygon = L.geoJSON(geojson, { style: polygonStyle })
                            editablepolygon.addTo(mapDelimit);
                            mapDelimit.fitBounds(editablepolygon.getBounds())
                        } else {
                            $('#intakeArea').val('');
                            return;
                        }
                    } catch (e) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error en archivo GeoJSON',
                            text: 'El archivo tiene carácteres erróneos o puede estar corrupto por favor intente con otro',
                        })
                        $('#intakeArea').val('');
                        return;
                    };
                };

                readerGeoJson.onerror = function() {
                    console.log(readerGeoJson.error);
                };
                readerGeoJson.readAsText(file);
            } else { //Zip
                var reader = new FileReader();
                reader.onload = function(evt) {
                    var contents = evt.target.result;
                    JSZip.loadAsync(file).then(function(zip) {
                        shapeValidation = validateShapeFile(zip);
                        shapeValidation.then(function(resultFile) {
                            //is valid shapefile
                            if (resultFile.valid) {
                                shp(contents).then(function(shpToGeojson) {
                                    geojson = shpToGeojson;
                                    delimitationFileType = delimitationFileEnum.SHP;
                                    let polygonStyle = {
                                        fillColor: "#337ab7",
                                        color: "#333333",
                                        weight: 0.2,
                                        fillOpacity: 0.3
                                    };
                                    editablepolygon = L.geoJSON(geojson, { style: polygonStyle })
                                    editablepolygon.addTo(mapDelimit);
                                    mapDelimit.fitBounds(editablepolygon.getBounds())
                                });
                            } else {
                                $('#intakeArea').val('');
                                return;
                            }
                        });
                        //loadShapefile(geojson, file.name);
                    }).catch(function(e) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error en shapefile',
                            text: 'Ha ocurrido un error de lectura en el shapefile',
                        })
                        console.log("Ocurrió error convirtiendo el shapefile " + e);
                        $('#intakeArea').val('');
                    });
                };
                reader.onerror = function(event) {
                    console.error("File could not be read! Code " + event.target.error.code);
                    //alert("El archivo no pudo ser cargado: " + event.target.error.code);
                };
                reader.readAsArrayBuffer(file);
            }
        } else { //Invalid extension
            Swal.fire({
                icon: 'error',
                title: 'Error de extensión',
                text: 'La extensión del archivo no está soportada, debe ser GeoJSON o un shapefile .zip',
            })
            $('#intakeArea').val('');
        }
    });
}
/** 
 * Get if file has a valid shape or GeoJSON extension 
 * @param {StriFileng} file   zip or GeoJSON file
 *
 * @return {Object} extension Object contain extension and is valid
 */
function validExtension(file) {
    var fileExtension = {};
    if (file.name.lastIndexOf(".") > 0) {
        var extension = file.name.substring(file.name.lastIndexOf(".") + 1, file.name.length);
        fileExtension.extension = extension;
    }
    if (file.type == 'application/x-zip-compressed' || file.type == 'application/zip') {
        fileExtension.valid = true;
    } else if (file.type == 'application/geo+json') {
        fileExtension.valid = true;
    } else {
        fileExtension.valid = false;
    }
    return fileExtension;
}

//draw polygons
drawPolygons = function() {
    // TODO: Next line only for test purpose
    //intakePolygons = polygons;

    lyrsPolygons.forEach(lyr => map.removeLayer(lyr));


    intakePolygons.forEach(feature => {
        let poly = feature.polygon;
        if (poly.indexOf("SRID") >= 0) {
            poly = poly.split(";")[1];
        }
        lyrsPolygons.push(omnivore.wkt.parse(poly).addTo(map));
    });
}