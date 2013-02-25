function getColumnFromCategory(cat_list, category) {
	var column = -1;
	for (var i = 0; i < cat_list.length; i += 4) {
		if (category == cat_list[i]) {
			column = Math.floor(i / 4) + 1;
		}
	}
//	console.log("getColumnForCategory(" + category + ") returns " + column);
	return column;
}

/**
 * Parses the string who's data is a python list with the format [["level", ["data1", ...]], [...]]
 * Works for both category and action data.
 * 
 * @param data a String in the SGG data format.  
 * @returns {Array} of the Level names.
 */
function getLevels(data) {
	var levels = [];
	var split = data.split('],');
	for (var i = 0; i < split.length; i++) {
		var start = split[i].indexOf('["');
		var end = split[i].indexOf('",');
		if (start != -1 && end != -1) {
			levels.push(split[i].slice(start + 2, end));
		}
	}
	return levels;
}

/**
 * Parses the data string, returning the list associated with the given level name. Works for both
 * category and action data.
 * 
 * @param level a String the name of the level.
 * @param data a String in the SGG data format
 * @returns {Array} of the list associated with the level, or false if level is not in the data.
 */
function getLevelList(level, data) {
//	console.log("getLevelList(" + level + ", " + data + ")");
	var split = data.split('],');
	for (var i = 0; i < split.length; i++) {
		var index = split[i].indexOf(level);
		if (index != -1) {
			var i2 = split[i].indexOf(']');
			var list = split[i].slice(index + level.length + 4, i2).split(', ');
//			console.log(list);
			return list;
		}
	}
	return false;
}

/**
 * Creates the save data string for the current Categories in the category dropzone.
 * @returns {String} The current categories as an encoded String.
 */
function createSGGCategorySaveData() {
	var levels = $('#sgg-grid .tab-pane');
	var temp = '';
	levels.each(function () {
		cat_value = temp;
		var level = $(this).attr('data-level');
		var slug = $(this).attr('data-slug');
		var levelStr = '"' + level + '"';
		var categories = $(this).find('#category-dropzone table tr');
		var children = categories.find("td div.sgg-category-drop");
		var inner_str =  '';
		for ( var i = 0; i < children.length; i++) {
			var child = $(children[i]);
			var cat_str = '"'.concat(child.data('slug'), '", ', child
					.data('priority'), ', "', trim1(child.text()), '", ' + child.data('pk'));
			inner_str = inner_str.concat(cat_str, ', ');
		}
		if (children.length > 0) {
			var tmp = inner_str.substr(0, inner_str.length - 2);
			var cat_list = levelStr.concat(', [', tmp, ']');
			cat_value = cat_value.concat('[' + cat_list + '], ');
			temp = cat_value;
		}

	});
	cat_value = temp;
	cat_value = cat_value.substr(0, cat_value.length - 2);
	cat_value = ''.concat('[' + cat_value + ']');
	return cat_value;
}

function handleCategoryDrop(event, ui) {
	var levelID = findLevelID(this);
	var column = $(this).data('column');
	var slug = ui.draggable.attr('data-slug');
	var pk = ui.draggable.attr('data-pk');
	if (pk == "-1") {
		$(this).html('');
		deactivateColumn(levelID, column);
	}
	else {
		var drop = createCategoryDropDiv(slug, column, ui.draggable.text(), trim2(pk));
		var html = $('<div />').append(drop.clone()).html();
		$(this).html(html);
		activateColumn(levelID, column, slug);
	}
	saveSggLayout();
}

function handleActionDrop(event, ui) {
	var column = $(this).data('column');
	var category = $(this).data('category');
	var row = $(this).data('row');
	var slug = ui.draggable.attr('id');
	var pk = ui.draggable.attr('data-pk');
	var type = ui.draggable.data('type');
	var unlock = ui.draggable.attr('data-unlock');
	if (type == "clear") {
		$(this).html('');
	} else if (type == "filler") {
		numFiller += 1;
		slug = 'filler-' + numFiller;
		var text = 'Filler-' + numFiller;
//		console.log("Dropping filler-" + numFiller + " slug=" + slug + ", category=" + category + ", type=" + type);
		var drop = createActionDropDiv(slug, type, row, column, category, text, "-1", "True");
		var html = $('<div />').append(drop.clone()).html();
		console.log(html);
		$(this).html(html);
		var listItem = $('.sgg-action [data-slug="' + trim2(slug) + '"][data-position="in-list"]');
		listItem.removeClass('draggable');
		listItem.attr('data-position=in-grid');		
	} else {
		var drop = createActionDropDiv(slug, type, row, column, category, ui.draggable.text(), pk, unlock);
		var html = $('<div />').append(drop.clone()).html();
		console.log(html);
		$(this).html(html);
		var listItem = $('.sgg-action [data-slug="' + trim2(slug) + '"][data-position="in-list"]');
		listItem.removeClass('draggable');
		listItem.attr('data-position=in-grid');
	}
	saveSggLayout();
}

/**
 * Creates the save data string for the current Actions in the action dropzone.
 * @returns {String} The current actions as an encoded String.
 */
function createSGGActionSaveData() {
	var levels = $('#sgg-grid .tab-pane');
	var act_value = '';
	var temp = '';
	levels.each(function () {
		act_value = temp;
		var level = $(this).attr('data-level');
		var slug = $(this).attr('id');
		var levelStr = '"' + level + '"';
		var actions = $(this).find('#action-dropzone table');
		var droppedActions = actions.find("td div.sgg-action");
		inner_str = '';
		for ( var j = 0; j < droppedActions.length; j++) {
			var action = $(droppedActions[j]);
			var act_slug = action.attr('data-slug');
			var category = action.attr('data-category');
			var pri = action.attr('data-priority');
			var type = action.attr('data-type');
			var pk = action.attr('data-pk');
			var act_str = '"'.concat(act_slug, '", "', type , '", "', category, '", ', pri, ', "', trim1(action.text()), '", ', pk);
			inner_str = inner_str.concat(act_str, ', ');
		}
		if (droppedActions.length > 0) {
			tmp = inner_str.substr(0, inner_str.length - 2);
			var act_list = levelStr.concat(', [' + tmp + ']');
			act_value = act_value.concat('[' + act_list + '], ');
			temp = act_value;
		}
	});
	act_value = temp;
	act_value = act_value.substr(0, act_value.length - 2);
	act_value = ''.concat('[' + act_value + ']');
	return act_value;
}


/**
 * Returns a jQuery object that represents the dropped Category.
 * @param slug a String the category's slug.
 * @param column an int the column the category is dropped into.
 * @param text a String the name of the Category.
 * @returns a jQuery object representing the dropped Category. It can be added to the page.
 */
function createCategoryDropDiv(slug, column, text, id) {
	console.log("createCategoryDropDiv(" + slug + ", " + column + ", " + text + ", " + id + ")");
	var drop = $('<div data-slug=' + trim1(slug) + ' class="sgg-category-drop" ' +
			'data-priority=' + column + '>' + '<a class="sgg-category" ' +
			'href="/challenge_admin/smartgrid/category/' + id + '/">'
			+ trim2(text) + '</a></div>');
	return drop;
} 

function clearSavedData() {
	deleteCookie('sgg_save');
	window.location.reload();
}

/**
 * Returns a jQuery object that represents the dropped Action.
 * @param slug a String the Action slug.
 * @param type a String the type of Action (Activity, commitment, event, filler)
 * @param row an int, the row the Action is in. This will become its priority.
 * @param column an int, the column the Action is in.
 * @param category a String the category slug.
 * @param text a String the name of the Action.
 * @returns a jQuery object representing the dropped Action.
 */
function createActionDropDiv(slug, type, row, column, category, text, id, unlock) {
	console.log("createActionDropDiv(" + slug + ", " + type + ", " + row + ", " + column + ", " + category + ", " + text + ", " + id + ", " + unlock + ")");
	var drop = $('<div data-slug="' + trim2(slug) + '" class="sgg-action sgg-' + trim2(type) + '-cell draggable" ' +
		   	'data-type="' + trim2(type) + '" data-priority="' + row + '" data-column="' + 
		   	column + '" data-category="' + trim2(category) + '" data-pk="' + trim2(id) + '" data-unlock="' + unlock + '">' +
		   	'<a href="/admin/smartgrid/' + trim2(type) + '/' + trim2(id) + '/"	class="sgg-action">' +
			trim2(text) + '</a></div>');
	return drop;
}

function activateColumn(levelID, column, slug) {
	console.log("activateColumn("+ levelID + ", " + column + ", " + slug + ")");
	for ( var i = 1; i < 11; i++) {
		var row = $('#' + levelID + ' .sgg-action-dropzone table tbody tr:nth-child(' + i + ')');
		var tdCell = row.find('td:nth-child(' + column + ')');
		var outerDiv = tdCell.children('div');
		outerDiv.removeClass('disabled');
		// Activate the div for dropping.
		outerDiv.droppable({
			accept : '.sgg-action',
			drop : handleActionDrop
		});
		outerDiv.attr('data-category', slug);
		var innerDiv = outerDiv.children('div');
		innerDiv.attr('data-category', slug);
	}		
}

function deactivateColumn(levelID, column) {
	console.log("deactivateColumn("+ levelID + ", " + column + ")");
	for ( var i = 1; i < 11; i++) {
		var row = $('#' + levelID + ' .sgg-action-dropzone table tbody tr:nth-child(' + i + ')');
		var tdCell = row.find('td:nth-child(' + column + ')');
		var outerDiv = tdCell.children('div');
		outerDiv.addClass('disabled');
		outerDiv.html('');
	}		
}

function saveSggLayout() {
	var cat_value = createSGGCategorySaveData();
	var hidden_category = $('#id_category_updates');
	hidden_category.attr('value', cat_value);
	var act_value = createSGGActionSaveData();
	var hidden_action = $('#id_action_updates');
	hidden_action.attr('value', act_value);
	setCookie('sgg_save', cat_value + act_value);
}

function loadSavedSGG(savedData) {
//	console.log("loadSavedSGG");
	var split = savedData.split('][');
	var categories = split[0];
//	console.log(categories);
	var actions = split[1];
//	console.log(actions);
	var levels = getLevels(categories);
//	console.log(levels);
	for (var i = 0; i < levels.length; i++) {
		var levelDiv = $('#sgg-level-' + (i + 1));
		var level = levelDiv.attr('id');
		var cat_list = getLevelList(levels[i], categories);
//		console.log(cat_list);
		var numCat = cat_list.length / 4;
		for (var j = 0; j < numCat * 4; j += 4) {
			var c = (j / 4) + 1;
			var dz = levelDiv.find('.sgg-category-slot[data-column="' + c + '"]');
//			console.log(dz);
			var slug = cat_list[j];
			var column = cat_list[j + 1];
			var text = cat_list[j + 2];
			var pk = cat_list[j + 3];
			var category = createCategoryDropDiv(slug, column, text, pk);
//			console.log($('<div />').append(category.clone()).html());
			dz.html($('<div />').append(category.clone()).html());
			activateColumn(level, c, slug);
		}
		var act_list = getLevelList(levels[i], actions);
//		console.log(act_list);
		for (var j = 0; j < act_list.length; j += 5) {
			var actIndex = Math.floor(j / 5);
//			var col = actIndex % numCat + 1;
			var row = Math.floor(actIndex / numCat) + 1;
			var slug = act_list[j];
			var type = act_list[j + 1];
			var category = act_list[j + 2];
			var rowStr = act_list[j + 3];
			var text = act_list[j + 4];
			var col = getColumnFromCategory(cat_list, category);
			console.log(slug + ", " + category + "[" + row + ", "+ col + " ]" + category + " " + text + " rowstr=" + rowStr);
			var dz = levelDiv.find('.sgg-action-slot[data-column="' + col +'"][data-row="' + rowStr + '"]');
//			console.log(dz);
			var action = createActionDropDiv(slug, type, rowStr, col, category, text);
			console.log($('<div />').append(action.clone()).html());
			dz.html($('<div />').append(action.clone()).html());
		}
	}
}
/**
 * Trims the whitespace from front and end of str.
 * @param str the string.
 * @returns The string without any spaces in the begging or end.
 */
function trim1 (str) {
    return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}

function trim2(str) {
	str = trim1(str);
	var i = str.indexOf('"');
	if (i == 0) {
		str = str.slice(i + 1, str.length - 1);
	}
	return str;
}

/**
 * Searches up the parent tree till data-level is found.
 * @param ele the child element.
 * @returns The level as a string.
 */
function findLevel(ele) {
	var p = ele.parentNode;
	
	while (p) {
		var level = $(p).attr('data-level');
		if (level) {
			return level;
		}
		p = p.parentNode;
	}
	return false;
}

function findLevelID(ele) {
	var p = ele.parentNode;
	
	while (p) {
		var level = $(p).attr('data-level');
		if (level) {
			return $(p).attr('id');
		}
		p = p.parentNode;
	}
	return false;
}	

function findLevelForSlug(slug) {
	var ele = $('div[data-slug=' + slug + ']');
	return false;
}