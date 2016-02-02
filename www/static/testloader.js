(function (cs) {
    "use strict";
    
    var slices = jsonresponse['arrays'].length;
    var imageArrayBase64 = [];
    for (var i = 0; i < slices; i++) {
      imageArrayBase64[i] = new Object();
      imageArrayBase64[i] = jsonresponse['arrays'][String(i)];
      
      var pixelDataAsString = window.atob(jsonresponse['arrays'][String(i)]['array']);
      var pixelData = str2ab(pixelDataAsString);
      imageArrayBase64[i].array = pixelData;
    };
    
    function str2ab(str) {
        var buf = new ArrayBuffer(str.length*2); // 2 bytes for each char
        var bufView = new Uint16Array(buf);
        var index = 0;
        for (var i=0, strLen=str.length; i<strLen; i+=2) {
            var lower = str.charCodeAt(i);
            var upper = str.charCodeAt(i+1);
            bufView[index] = lower + (upper <<8);
            index++;
        }
        return bufView;
    };

    function getExampleImage(imageId) {
        id = imageid.split("//")[-1];
        function getPixelData()
        {
            id = imageid.split("//")[-1];
            return imageArrayBase64[id];
           
        }

        var image = {
            imageId: imageId,
            minPixelValue : imageArrayBase64[id].min,
            maxPixelValue : imageArrayBase64[id].max,
            slope: 1.0,
            intercept: 0,
            windowCenter : 257,
            windowWidth : 512,
            render: cornerstone.renderGrayscaleImage,
            getPixelData: getPixelData,
            rows: imageArrayBase64[id].height,
            columns: imageArrayBase64[id].width,
            height: imageArrayBase64[id].height,
            width: imageArrayBase64[id].width,
            color: false,
            columnPixelSpacing: imageArrayBase64[id].column_spacing,
            rowPixelSpacing: imageArrayBase64[id].row_spacing,
            sizeInBytes: imageArrayBase64[id].width * imageArrayBase64[id].height * 2
        };

        var deferred = $.Deferred();
        deferred.resolve(image);
        return deferred;
    }


    // register our imageLoader plugin with cornerstone
    cs.registerImageLoader('example', getExampleImage);

}(cornerstone));