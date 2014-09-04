// Global variables
var table;        // Table object
var rowArray = new Array();   // Data row array
var titleRowArray = new Array();  // Contains title texts
var titleRowCellArray = new Array();  // Dynamically constructed title cells
var titleSpanCellArray = new Array(); // Title elelments from row-spanned
var colSpanArray = new Array();   // Rows col-spanned
var colTitleFilled = new Array(); // Indicates whether title is filled
var sortIndex;        // Selected index for sort
var descending = false;     // Descending order
var nRow, actualNRow, maxNCol;    // Various table stats
var origColor;        // Holds original default color
var isIE;       // True if IE
var linkEventString =     // What's insider <a> tag
  'onMouseOver=\'setCursor(this);' +
  'setColor(this,"selected");\' ' +
  'onMouseOut=\'setColor(this,"default");\' ' +
  'onClick=\'sortTable(';

// Configurable constants
var ascChr = "^";     // Symbol for ascending sort
var desChr = "v";     // Symbol for descending sort
var selectedColor = "black";   // Color for sort focus
var defaultColor = "black";   // Default color for sort off-focus
var recDelimiter = '|';     // Char used as a record separator
var titleFace = 'b';      // Specifies the HTML tag for titles
var updownColor = 'gray';   // Specified the color for up/downs 

//*****************************************************************************
// Main function. This is to be associated with onLoad event in <BODY>. 
//
// IMPORTANT: This is the only function that needs to be included in the pages
// to be sorted. The rest of the functions are simply called by this
// function.
//*****************************************************************************
function initTable(obj)
{
  // Check whether it's viewed by IE 5.0 or greater
  if (! checkBrowser()) return;

  // Local variables
  var countCol;
  var nChildNodes;
  var innerMostNode;
  var nColSpan, nRowSpannedTitleCol, colPos;
  var cell, cellText;
  var titleFound = false;
  var rNRowSpan, rNColSpan;

  // Initializing global table object variable
  if (obj.tagName == "TABLE")
  {
    // Assumes that the obj is THE OBJECT
    table = obj;
  }
  else
  {
    // Assumes that the obj is the id of the object
    table = document.getElementById(obj);
  }

  // Check whether it's an object
  if (table == null) return;

  // Check whether it's a table
  if (table.tagName != "TABLE") return;

  // Initializing the max col number with the size of last data row
  maxNCol = table.rows[table.rows.length-1].cells.length;

  // Initializing arrays
  rowArray = new Array();
  colSpanArray = new Array();
  colTitleFilled = new Array();
  titleRowArray = new Array();
  titleRowCellArray = new Array();
  
  for (var i=0; i<maxNCol; i++)
    colTitleFilled[i] = false;

  // Setting the number of rows
  nRow = table.rows.length; 

  // Should have at least 1 row
  if (nRow < 1) return;

  // Initialization of local variables
  actualNRow = 0;     // Number of actual data rows
  rNRowSpan = 0;      // Remaining rows in the row span
  rNColSpan = 0;      // Remaining cols in the col span
  nRowSpannedTitleCol = 0;  // Number of title cols from row span
    
  // Loop through rows
  for (var i=0; i<nRow; i++)
  {
    nColSpan = 1, colPos = 0;
    // Loop through columns
    // Initializing
    for (var j=0; j<table.rows[i].cells.length; j++)
    {
      // Do this iff title has not been found
      if (titleFound == false)
      {
        if (table.rows[i].cells[j].rowSpan > 1)
        {
          if (table.rows[i].cells[j].colSpan < 2)
          {
            titleSpanCellArray[colPos] =
              table.rows[i].cells[j];
            colTitleFilled[colPos] = true;
            nRowSpannedTitleCol++;
          }
          if (table.rows[i].cells[j].rowSpan - 1 
            > rNRowSpan)
          {
            rNRowSpan = 
              table.
              rows[i].cells[j].
              rowSpan - 1;

            if (table.rows[i].
              cells[j].colSpan > 1)
              rNColSpan = 
                rNRowSpan + 1;
          }
        }
      }
      if (table.rows[i].cells[j].colSpan > 1 &&
        rNColSpan == 0)
      { 
        nColSpan = table.rows[i].cells[j].colSpan;
        colPos += nColSpan;
      }
      else
      {
        colPos++;
      }   
    }
          
    // Setting up the title cells
    if (titleFound == false && nColSpan == 1 && 
      rNRowSpan == 0 && rNColSpan == 0 && titleFound == false)
    {
      colSpanArray[i] = true;
      titleFound = true;

      // Using indivisual cell as an array element
      countCol = 0;
      for (var j=0; 
        j<table.rows[i].cells.length
          + nRowSpannedTitleCol; j++)
      {
        if (colTitleFilled[j] != true)
        {
          titleRowCellArray[j] =
            table.rows[i].cells[countCol];
          countCol++;
        }
        else
        {
          titleRowCellArray[j] = 
            titleSpanCellArray[j];
        }
      }
    }
    // Setting up the data rows
    else if (titleFound == true && nColSpan == 1 && rNRowSpan == 0)
    {
      for (var j=0; j<table.rows[i].cells.length; j++)
      {
        // Can't have row span in record rows ...
        if (table.rows[i].cells[j].rowSpan > 1) return;
        nChildNodes =
          table.rows[i].
          cells[j].firstChild.childNodes.
          length;

        innerMostNode = 
          table.rows[i].
          cells[j].firstChild;

        while ( nChildNodes != 0)
        {
          innerMostNode =
            innerMostNode.
            firstChild;
          nChildNodes =
            innerMostNode.
            childNodes.
            length;
        }

        if (j == 0)
        {
          rowArray[actualNRow] = 
            innerMostNode.data;
        }
        else
        {
          rowArray[actualNRow] += recDelimiter +
            innerMostNode.data;
        }
      }
      // Inconsistent col lengh for data rows
      if (table.rows[i].cells.length > maxNCol)
        return;
      actualNRow++;
      colSpanArray[i] = false;
    }
    else if (nColSpan == 1 && rNRowSpan == 0 && 
      rNColSpan == 0 && titleFound == false)
    {
      colSpanArray[i] = false;
    }
    else
    {
      colSpanArray[i] = true;
    }
    
    // Counters for row/column spans
    if (rNRowSpan > 0) rNRowSpan--;
    if (rNColSpan > 0) rNColSpan--;
  }

  // If the row number is < 1, no need to do anything ...
  if (actualNRow < 1) return;

  // Re-drawing the title row
  for (var j=0; j<maxNCol; j++)
  {
    // If for some reason, the rows do NOT have any child, then
    // simply return ...
    if (titleRowCellArray[j].childNodes.length == 0) return;
    if (titleRowCellArray[j].firstChild != null)
    {
      nChildNodes = 
        titleRowCellArray[j].
        firstChild.childNodes.length;
      innerMostNode = 
        titleRowCellArray[j].firstChild;

      while ( nChildNodes != 0)
      {
        innerMostNode =
          innerMostNode.firstChild;
        nChildNodes =
          innerMostNode.
          childNodes.
          length;
      }
      cellText = innerMostNode.data;
    }
    else
    {
      cellText = "column(" + j + ")";
    }
    titleRowArray[j] = cellText;
    titleRowCellArray[j].innerHTML =
      '<a ' +
      linkEventString +
      j + ',' + '"' + table.id + '"' + ');\'>' + 
      '<' + titleFace + '>' + cellText + 
      '</' + titleFace +'></a>';
  }
}

//*****************************************************************************
// Function called when user clicks on a title to sort
//*****************************************************************************
function sortTable(index,obj)
{
  // Re-inializing the table object
  initTable(obj);

  // Local variables
  var nChildNodes;
  var innerMostNode;
  var rowContent;
  var rowCount;
  var cell, cellText;
  var newTitle;
  
  // Can't sort past the max allowed column size
  if (index < 0 || index >= maxNCol) return;
  
  // Assignment of sort index
  sortIndex = index;
  // Doing the sort using JavaScript generic function for an Array
  rowArray.sort(compare);

  // Re-drawing the title row
  for (var j=0; j<maxNCol; j++)
  {
    cellText = titleRowArray[j];
    cellText = '<' + titleFace +'>' +
      cellText + '</' + titleFace + '></a>';
    newTitle = '<a ' +
      linkEventString +
      j + ',' + '"' + table.id + '"' + ');\'>' +
      cellText +
      '</a>';
    if (j == sortIndex)
    {
      newTitle += '&nbsp;<font color=' + updownColor + '>';
      if (descending)
        newTitle += desChr;
      else
        newTitle += ascChr;
      newTitle += '</font>';
    }
    titleRowCellArray[j].innerHTML = newTitle;
  }

  // Re-drawing the table
  rowCount = 0;
  for (var i=0; i<nRow; i++)
  {
    if (! colSpanArray[i])
    {
      for (var j=0; j<maxNCol; j++)
      {
        rowContent = rowArray[rowCount].
          split(recDelimiter);
        nChildNodes =
          table.rows[i].cells[j].firstChild.
          childNodes.length;
        innerMostNode = 
          table.rows[i].cells[j].firstChild;

        while ( nChildNodes != 0)
        {
          innerMostNode =
            innerMostNode.firstChild;
          nChildNodes =
            innerMostNode.
            childNodes.
            length;
        }
        innerMostNode.data = rowContent[j];
      }
      rowCount++;
    }
  }

  // Switching btw descending/ascending sort
  if (descending)
    descending = false;
  else
    descending = true;
}

//*****************************************************************************
// Function to be used for Array sorting
//*****************************************************************************
function compare(a, b)
{
  // Getting the element array for inputs (a,b)
  var aRowContent = a.split(recDelimiter);
  var bRowContent = b.split(recDelimiter);
  
  // Needed in case the data conversion is necessary
  var aToBeCompared, bToBeCompared;

  if (! isNaN(aRowContent[sortIndex]))
    aToBeCompared = parseInt(aRowContent[sortIndex], 10);
  else
    aToBeCompared = aRowContent[sortIndex];

  if (! isNaN(bRowContent[sortIndex]))
    bToBeCompared = parseInt(bRowContent[sortIndex], 10);
  else
    bToBeCompared = bRowContent[sortIndex];

  if (aToBeCompared < bToBeCompared)
    if (!descending)
    {
      return -1;
    }
    else
    {
      return 1;
    }
  if (aToBeCompared > bToBeCompared)
    if (!descending)
    {
      return 1;
    }
    else
    {
      return -1;
    }
  return 0;
}

//*****************************************************************************
// Function to set the cursor
//*****************************************************************************
function setCursor(obj)
{
  // Show hint text at the browser status bar
  window.status = "Sort by " + obj.firstChild.innerHTML;
  // Change the mouse cursor to hand or pointer
  if (isIE)
    obj.firstChild.style.cursor = "hand";
  else
    obj.firstChild.style.cursor = "pointer";
}

//*****************************************************************************
// Function to set the title color
//*****************************************************************************
function setColor(obj,mode)
{
  if (mode == "selected")
  {
    // Remember the original color
    if (obj.style.color != selectedColor) 
      defaultColor = obj.style.color;
    obj.style.color = selectedColor;
  }
  else
  { 
    // Restoring original color and re-setting the status bar
    obj.style.color = defaultColor;
    window.status = '';
  }
}

//*****************************************************************************
// Function to check browser type/version
//*****************************************************************************
function checkBrowser()
{
  if (navigator.appName == "Microsoft Internet Explorer"
    && navigator.appVersion.indexOf("5.") >= 0)
  {
    isIE = true;
    return true;
  }
  // For some reason, appVersion returns 5 for Netscape 6.2 ...
  else if (navigator.appName == "Netscape"
    && navigator.appVersion.indexOf("5.") >= 0)
  {
    isIE = false;
    return true;
  }
  else
    return false;
}
