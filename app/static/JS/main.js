$(document).ready(function () {
	//save
	$(".saveButton").on("click", function (e) {
		e.preventDefault();

		item_counter_list = $("#item_counter_list").val();
		arrayvalue = item_counter_list.split(",");
		orderItems = [];
		customerId = $("#customer_id").val();
		console.log("customer_id", customerId);
		grand_total = $("#grand_total").val();
		if (parseInt(grand_total) === 0) {
			alert("There is no grand total");
			return;
		}
		if (!customerId) {
			alert("Please select customer");
			return;
		}
		main_percent_input = $("#main_percent_input").val();
		main_amount_input = $("#main_amount_input").val();
		grand_total = $("#grand_total").val();
		if (parseInt(grand_total) === 0) {
			alert("Please select some products");
			return;
		}

		$.each(arrayvalue, function (index, value) {
			obj = {};
			obj["product"] = $("#item_id_" + value).val();
			obj["percent_input"] = $("#percent_input_" + value).val();
			obj["amount_input"] = $("#amount_input_" + value).val();
			obj["product_description"] = $("#item_desc_" + value).text();
			obj["item_quantity"] = $("#item_quantity_" + value).val();
			obj["unit_price"] = $("#unit_price_" + value).val();
			obj["sub_total"] = $("#sub_total_" + value).val();

			orderItems.push(obj);
		});

		console.log(typeof orderItems);
		var data = {};
		data["myObjects"] = orderItems;
		data["customer_id"] = customerId;
		data["main_percent_input"] = main_percent_input;
		data["main_amount_input"] = main_amount_input;
		data["grand_total"] = grand_total;

		convertedData = JSON.stringify(data);
		$.ajax({
			method: "POST",
			url: "/save-order",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(data),
			success: function (res, status, xhr) {
				console.log("ananta last");
			},
		});
		window.location.replace("/orders");
	});
});

//change main discount checkbox
function mainDiscountCheckBox() {
	if ($(".main_discount").is(":checked")) {
		$(`#main_amount_input`).css("display", "block");
		$(`#main_percent_input`).css("display", "none");
		$(`#main_percent_input`).val("");
		calculate_total();
	} else {
		$(`#main_amount_input`).css("display", "none");
		$(`#main_percent_input`).css("display", "block");
		$(`#main_amount_input`).val("");
		calculate_total();
	}
}
function changeDiscountInput(data_id) {
	id = data_id;
	isProductSelected = $("#item_id_" + id).val();
	if (parseInt(isProductSelected) > 0) {
		quantity = parseInt($("#item_quantity_" + id).val());
		if (quantity > 0) {
			if ($("#is_discount_amount_" + id).is(":checked")) {
				console.log("small amount checked");
				unit_price = $("#unit_price_" + id).val();

				sub_total = quantity * unit_price;

				sub_total = parseFloat(sub_total).toFixed(2);
				$("#sub_total_" + id).val(sub_total);
				calculate_total();
				$(`#amount_input_${id}`).css("display", "block");
				$(`#percent_input_${id}`).css("display", "none");
				$(`#percent_input_${id}`).val("");
				if ($(".main_discount").is(":checked")) {
					mainAmountDiscount();
				} else {
					mainPercentDiscount();
				}
			} else {
				console.log("small discount checked");
				unit_price = $("#unit_price_" + id).val();

				sub_total = quantity * unit_price;
				sub_total = parseFloat(sub_total).toFixed(2);
				$("#sub_total_" + id).val(sub_total);
				calculate_total();
				$(`#amount_input_${id}`).css("display", "none");
				$(`#percent_input_${id}`).css("display", "block");
				$(`#amount_input_${id}`).val("");
				if ($(".main_discount").is(":checked")) {
					mainAmountDiscount();
				} else {
					mainPercentDiscount();
				}
			}
		} else {
			alert("please select quantity");
			$("#is_discount_amount_" + id).prop("checked", false);
		}
	} else {
		alert("please select product");
		$("#is_discount_amount_" + id).prop("checked", false);
	}
}

function percentInput(data_id) {
	id = data_id;
	console.log("data_id", id);
	value = $("#percent_input_" + id).val();
	console.log("discount", value);
	quantity = parseInt($("#item_quantity_" + id).val());
	if (quantity === 0) {
		alert("please input quantity number");
		$(this).val("");
		return;
	} else {
		unit_price = $("#unit_price_" + id).val();
		sub_total = quantity * unit_price;
		if (value) {
			var disc = parseFloat(value / 100) * parseFloat(sub_total);
			discounted_amount = parseFloat(sub_total) - parseFloat(disc);
			sub_total = parseFloat(discounted_amount).toFixed(2);
			console.log("sub_total", sub_total);
			$("#sub_total_" + id).val(sub_total);
			calculate_total();
			if ($(".main_discount").is(":checked")) {
				mainAmountDiscount();
			} else {
				mainPercentDiscount();
			}
		} else {
			$("#sub_total_" + id).val(sub_total);
		}
	}
}

function amountInput(data_id) {
	id = data_id;
	value = $("#amount_input_" + id).val();
	quantity = parseInt($("#item_quantity_" + id).val());
	if (quantity === 0) {
		alert("please input quantity number");
		$("#amount_input_" + id).val("");
	} else {
		unit_price = $("#unit_price_" + id).val();

		sub_total = quantity * unit_price;
		discounted_amount = parseFloat(sub_total) - parseFloat(value);
		sub_total = parseFloat(discounted_amount).toFixed(2);

		$("#sub_total_" + id).val(sub_total);
		calculate_total();
		if ($(".main_discount").is(":checked")) {
			mainAmountDiscount();
		} else {
			mainPercentDiscount();
		}
		return sub_total;
	}
}

function mainAmountDiscount() {
	value = $("#main_amount_input").val();
	var item_counters = $("#item_counter").val();
	var item_counter_list = $("#item_counter_list").val();
	var itemList = getItemAsList(item_counter_list);
	total = 0;
	for (i = 0; i < item_counters; i++) {
		var item = itemList[i];
		if (item === undefined) {
		} else {
			sub_total = $("#sub_total_" + item).val();
			total = parseFloat(total) + parseFloat(sub_total);
		}
	}
	total = parseFloat(total).toFixed(2);
	grand_total = total;
	if (parseInt(grand_total) === 0) {
		alert("there is no grand total");
	} else {
		console.log("main Amount discount");
		discounted_amount = parseFloat(grand_total) - parseFloat(value);
		$("#grand_total").val(parseFloat(discounted_amount).toFixed(2));
	}
}

function mainPercentDiscount() {
	value = $("#main_percent_input").val();
	var item_counters = $("#item_counter").val();
	var item_counter_list = $("#item_counter_list").val();
	var itemList = getItemAsList(item_counter_list);
	total = 0;
	for (i = 0; i < item_counters; i++) {
		var item = itemList[i];
		if (item === undefined) {
		} else {
			sub_total = $("#sub_total_" + item).val();
			total = parseFloat(total) + parseFloat(sub_total);
		}
	}
	total = parseFloat(total).toFixed(2);
	grand_total = total;
	if (parseInt(grand_total) === 0) {
		alert("there is no grand total");
	} else {
		console.log("main percent discount");
		var disc = parseFloat(value / 100) * parseFloat(grand_total);
		discounted_amount = parseFloat(grand_total) - parseFloat(disc);
		$("#grand_total").val(parseFloat(discounted_amount).toFixed(2));
	}
}

$(function () {
	// Start counting from the third row
	var table = document.getElementById("po_table");
	var tbodyRowCount = table.tBodies[0].rows.length; // 3
	var counter = tbodyRowCount;
	var itemlist = "";

	$("#insertRow").on("click", function (event) {
		event.preventDefault();
		var item_counter_list = $("#item_counter_list").val();
		itemList = getItemAsList(item_counter_list);
		item_count = itemList.length;
		console.log("item_count", item_count);
		value = $("#item_id_" + itemList.length).val();
		if (!value) {
			alert("please select product for previous row");
			return;
		}

		console.log("ya chircha ke");

		//var item_array = item_counter_list.split(",");
		event.preventDefault();

		var newRow = $("<tr>");
		var cols = "";

		// Increase counter after each row insertion
		counter++;
		// Table columns
		$("#item_counter").val(counter);
		itemList.push(counter);
		cols += `<td>
                                <div class="btn-group bootstrap-select">
                                  <div id="vendor_item_list_${counter}">
                                    <select class="selectpicker dropup" data-container="body" data-live-search="true" name="item_id_${counter} " id="item_id_${counter}" title="Select Item..." onchange="populateItemDetails(this.value,this.name)" required>
                                    
                                    </select>
                                  </div>
                                </div>
                              </td>
                              <td id="item_desc_${counter}">description</td>
                              <td class="text-left">
                                <input type="number" class="form-control" onchange="calculate_item_total(this.name)" value="0" name="item_quantity_${counter}" id="item_quantity_${counter}"/>
                              </td>
                              <td class="text-right">
                                <div class="input-group mb-3">
                                  <span class="input-group-text border-0 bg-white" id="basic-addon1">$</span>
                                  <input class="form-control-plaintext" type="number" name="unit_price_${counter}" id="unit_price_${counter}" value="0" readonly></input>
                                </div>
                              </td>
                              <td>
                                <label><input type="checkbox" name="is_wholesale" value="1" id="is_discount_amount_${counter}" class="is_discount_amount" data-id="${counter}" onclick=changeDiscountInput(${counter})>Amount?</label>
                       
                                </td>
                              <td>
                                <input type="number" onchange=percentInput(${counter}) id="percent_input_${counter}" placeholder="%" class="form-control percent_input" data-id="${counter}" style="display:block"/>

                                <input type="text" onchange=amountInput(${counter}) id="amount_input_${counter}" placeholder="$" class="form-control hidden amount_input" style="display:none" data-id="${counter}"/>
                              </td>
                              
                              <td class="text-left border-left">
                                <div class="input-group mb-3">
                                  <span class="input-group-text border-0 bg-white" id="basic-addon1">$</span>
                                  <input class="form-control-plaintext" type="number" name="sub_total_${counter}" id="sub_total_${counter}" value="0" readonly></input> 
                                </div>
                                </td>`;
		cols += `<td class="text-right"><a class="btn btn-sm danger" id ="deleteRow_${counter}" onclick="remove_po_item(this.id)"><i class="fa fa-remove"></i></a></td>`;

		// Insert the columns inside a row
		newRow.append(cols);

		// Insert the row inside a table
		$("#po_table").append(newRow);
		$("#item_counter_list").val(itemList);
		$.ajax({
			type: "GET",
			url: "/get-products-for-order",
			success: function (data, status, xhr) {
				populateDropdown(data);
				$(".selectpicker").selectpicker("refresh");
			},
		});

		$(".selectpicker").selectpicker("refresh");
	});
});

function getItemAsList(string) {
	return string.toString().split(",");
}
function removeFromArray(array, item) {
	var index = array.indexOf(item);
	if (index > -1) {
		// only splice array when item is found
		array.splice(index, 1); // 2nd parameter means remove one item only
	}
	return array;
}
function calculate_total() {
	var item_counters = $("#item_counter").val();
	var item_counter_list = $("#item_counter_list").val();
	var itemList = getItemAsList(item_counter_list);
	total = 0;
	for (i = 0; i < item_counters; i++) {
		var item = itemList[i];
		if (item === undefined) {
		} else {
			sub_total = $("#sub_total_" + item).val();
			total = parseFloat(total) + parseFloat(sub_total);
		}
	}
	total = parseFloat(total).toFixed(2);
	$("#grand_total").val(total);
}

function populateItemDetails(value, name) {
	console.log(name);
	var row_num = name.split("_").slice(-1)[0];
	$.ajax({
		type: "GET",
		url: "/populateItems/" + value,
		success: function (data, status, xhr) {
			console.log("ananta", data);
			$("#item_desc_" + row_num).text(data.description);
			unit_price = parseFloat(data.sales_price).toFixed(2);
			$("#unit_price_" + row_num).val(unit_price);
		},
	});
}
function populateDropdown(data) {
	html = "";
	var item_counters = $("#item_counter").val();

	if (jQuery.isEmptyObject(data)) {
		for (var i = 1; i <= parseInt(item_counters); i++) {
			html = '<select class="selectpicker dropup" style="display: block !important" data-container="body" data-live-search="true" name="item_id_' + i + '" id="item_id_' + i + '" title="Select Item..." onchange="populateItemDetails(this.value,this.name)" required></select>';
			$("#vendor_item_list_" + i)
				.html(html)
				.selectpicker("refresh");
			$("#item_desc_" + i).val("");
			$("#item_quantity_" + i).val(0);
			$("#unit_price_" + i).val(0);
			$("#sub_total_" + i).val(0);
		}
	} else {
		var options = "";
		$.each(data, function (idx, obj) {
			options += '<option value="' + obj.product_id + '">' + obj.product_code + "</option>";
		});

		for (var i = 1; i <= parseInt(item_counters); i++) {
			html = '<select class="selectpicker dropup" style="display: block !important" data-container="body" data-live-search="true" name="item_id_' + i + '" id="item_id_' + i + '" title="Select Item..." onchange="populateItemDetails(this.value,this.name)" required>' + options + "</select>";

			var selectVal = $("#item_id_" + i).val();
			if (!selectVal) {
				$("#vendor_item_list_" + i)
					.html(html)
					.selectpicker("refresh");
			}
		}
	}
}

function populateItems() {
	$.ajax({
		type: "GET",
		url: "/get_vendor_items?id=" + value,
		success: function (data, status, xhr) {
			populateDropdown(data);
			$(".selectpicker").selectpicker("refresh");
		},
	});
}

// Remove row when delete btn is clicked
/* $("table").on("click", "#deleteRow", function (event) {
          $(this).closest("tr").remove();
          counter -= 1
          $("#item_counter").val(counter);
          calculate_total();
      });
      */

function remove_po_item(value) {
	console.log(value);
	var itemList = getItemAsList($("#item_counter_list").val());

	var row_num = value.split("_").slice(-1)[0];
	var counter = $("#item_counter").val();
	$("#deleteRow_" + row_num)
		.closest("tr")
		.remove();
	counter -= 1;
	$("#item_counter").val(counter);
	itemList = removeFromArray(itemList, row_num);
	console.log("itemList", itemList);
	$("#item_counter_list").val(itemList);
	calculate_total();
	grand_total = $("#grand_total").val();
	if (parseInt(grand_total) > 0) {
		console.log("ya chiryo");
		if ($(".main_discount").is(":checked")) {
			mainAmountDiscount();
		} else {
			mainPercentDiscount();
		}
	}
}

function calculate_item_total(name) {
	var row_num = name.split("_").slice(-1)[0];
	product = $("#item_id_" + row_num).val();
	// there should be product to increase quantity
	if (product) {
		quantity = parseInt($("#item_quantity_" + row_num).val());
		console.log("quantity", quantity);
		unit_price = $("#unit_price_" + row_num).val();
		sub_total = quantity * unit_price;
		console.log("subbbb", sub_total);
		sub_total = parseFloat(sub_total).toFixed(2);
		let new_sub_total = null;
		console.log("#is_discount_amount_" + row_num);
		if ($("#is_discount_amount_" + row_num).is(":checked")) {
			console.log("checked");
			amountInput(row_num);
		} else {
			console.log("not checked");
			percentInput(row_num);
		}

		calculate_total();
		grand_total = $("#grand_total").val();
		if (parseInt(grand_total) > 0) {
			console.log("ya chiryo");
			if ($(".main_discount").is(":checked")) {
				mainAmountDiscount();
			} else {
				mainPercentDiscount();
			}
		}
	} else {
		alert("please select product");
		$("#item_quantity_" + row_num).val("");
		return;
	}
}

function calculate_total() {
	var item_counters = $("#item_counter").val();
	var item_counter_list = $("#item_counter_list").val();
	var itemList = getItemAsList(item_counter_list);
	total = 0;
	for (i = 0; i < item_counters; i++) {
		var item = itemList[i];
		if (item === undefined) {
		} else {
			sub_total = $("#sub_total_" + item).val();
			total = parseFloat(total) + parseFloat(sub_total);
		}
	}
	total = parseFloat(total).toFixed(2);
	$("#grand_total").val(total);
}

function initialize() {
	var latlng = new google.maps.LatLng(27.732323, 85.326601);
	var map = new google.maps.Map(document.getElementById("map"), {
		center: latlng,
		zoom: 13,
	});
	var marker = new google.maps.Marker({
		map: map,
		position: latlng,
		draggable: true,
		anchorPoint: new google.maps.Point(0, -29),
	});
	var input = document.getElementById("searchInput");
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
	var geocoder = new google.maps.Geocoder();
	var autocomplete = new google.maps.places.Autocomplete(input);
	autocomplete.bindTo("bounds", map);
	var infowindow = new google.maps.InfoWindow();
	autocomplete.addListener("place_changed", function () {
		infowindow.close();
		marker.setVisible(false);
		var place = autocomplete.getPlace();
		console.log(place.address_components);
		console.log(place.address_components.at(-2));
		var reserved = 4;
		address_place = parseInt(place.address_components.length) - parseInt(reserved);
		combined_address = "";
		for (i = 0; i < address_place; i++) {
			combined_address += place.address_components[i].long_name + ", ";
		}
		console.log("combined", combined_address.slice(0, -2));

		if (!place.geometry) {
			window.alert("Autocomplete's returned place contains no geometry");
			return;
		}

		// If the place has a geometry, then present it on a map.
		if (place.geometry.viewport) {
			map.fitBounds(place.geometry.viewport);
		} else {
			map.setCenter(place.geometry.location);
			map.setZoom(17);
		}

		marker.setPosition(place.geometry.location);
		marker.setVisible(true);

		bindDataToForm(
			place.formatted_address,
			place.geometry.location.lat(),
			place.geometry.location.lng(),

			place.address_components.at(-2),
			place.address_components.at(-3),
			place.address_components.at(-4),

			place.address_components.at(-1),
			combined_address
		);
		infowindow.setContent(place.formatted_address);
	});
}
function bindDataToForm(address, lat, lng, country, state, city, postal_code, combined_address) {
	document.getElementById("location").value = address;
	document.getElementById("country").value = country.long_name;
	document.getElementById("address1").value = combined_address.slice(0, -2);
	document.getElementById("city").value = city.long_name;
	document.getElementById("state").value = state.long_name;
	document.getElementById("post_code").value = postal_code.long_name;
}
google.maps.event.addDomListener(window, "load", initialize);

$(".addCustomer").on("click", function (e) {
	e.preventDefault();
	$(".myModal").modal("show");
});
$(".saveCustomer").on("click", function (e) {
	e.preventDefault();
	$("#exampleModal-1").addClass("show");
	$("#exampleModal-1").removeClass("hide");
	$(".modal-backdrop").addClass("show");
	$(".modal-backdrop").removeClass("hide");
	first_name = $("#first_name").val();
	last_name = $("#last_name").val();
	email = $("#email").val();
	company = $("#company").val();
	phone = $("#phone").val();
	l1 = $("#location").val();
	country = $("#country").val();
	address1 = $("#address1").val();
	address2 = $("#address2").val();
	city = $("#city").val();
	state = $("#state").val();
	postcode = $("#postcode").val();
	is_wholesale = $("#is_wholesale").val();
	if ($("#is_wholesale").is(":checked")) {
		is_wholesale = 1;
	} else {
		is_wholesale = 0;
	}
	$.ajax({
		url: "/save-customer",
		contentType: "application/json;charset=UTF-8",
		data: JSON.stringify({
			first_name: first_name,
			last_name: last_name,
			email: email,
			company: company,
			phone: phone,
			l1: l1,
			country: country,
			address1: address1,
			address2: address2,
			city: city,
			state: state,
			postcode: postcode,
			is_wholesale: is_wholesale,
		}),
		method: "post",
		success: function (data) {
			$(".myModal").modal("hide");
			$("#first_name").val("");
			$("#last_name").val("");
			$("#email").val("");
			$("#company").val("");
			$("#phone").val("");
			$("#location").val("");
			$("#country").val("");
			$("#address1").val("");
			$("#address2").val("");
			$("#city").val("");
			$("#state").val("");
			$("#postcode").val("");
			$("#item_id_222").append('<option value="' + data.id + '" selected>' + data.first_name + " " + data.last_name + "</option>");
			$("#item_id_222").selectpicker("refresh");
		},
	});
});
