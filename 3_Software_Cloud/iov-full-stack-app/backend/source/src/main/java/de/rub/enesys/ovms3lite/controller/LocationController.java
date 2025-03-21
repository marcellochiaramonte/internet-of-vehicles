package de.rub.enesys.ovms3lite.controller;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import de.rub.enesys.ovms3lite.dto.input.LocationInput;
import de.rub.enesys.ovms3lite.dto.output.LocationForList;
import de.rub.enesys.ovms3lite.model.Location;
import de.rub.enesys.ovms3lite.service.LocationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@RestController
public class LocationController extends BaseRestController{

    @Autowired
    private LocationService locationService;

    @PostMapping("location/new")
    Location createNewEvent(
            @RequestParam Long timestamp,
            @RequestParam Double latitude,
            @RequestParam Double longitude,
            @RequestParam String carId
    ){
        return locationService.createNewLocation(timestamp,latitude,longitude,carId);
    }

    @GetMapping("location/filter")
    List<LocationForList> filterLocationsByTimestamp(
            @RequestParam String carId,
            @RequestParam Long startTimestamp,
            @RequestParam Long endTimestamp
    ){
    return locationService.filterLocations(carId, startTimestamp,endTimestamp);
    }

    @GetMapping("location/current")
    LocationForList filterLocationsByTimestamp(
            @RequestParam String carId
    ){
        return locationService.getLastLocation(carId);
    }

    @PostMapping("location/new/multiple")
    ResponseEntity createMultipleEvents(
            @RequestParam String carId,
            @RequestBody String dataList
    ) throws IOException {
//        System.out.println(dataList);
        ObjectMapper mapper = new ObjectMapper();
        List<LocationInput> list = new ArrayList<>();
        ResponseEntity response = new ResponseEntity<>(HttpStatus.OK);
        try{
            JsonParser parser = mapper.getFactory().createParser(dataList);
            if(parser.nextToken() != JsonToken.START_ARRAY) {
                throw new IllegalStateException("Expected an array");
            }
            while(parser.nextToken() == JsonToken.START_OBJECT) {
                // read everything from this START_OBJECT to the matching END_OBJECT
                // and return it as a tree model ObjectNode
                ObjectNode node = mapper.readTree(parser);
                LocationInput locationInput = new LocationInput();
                locationInput.setT(node.get("t").asLong());
                locationInput.setLat(node.get("lat").asDouble());
                locationInput.setLon(node.get("lon").asDouble());
                list.add(locationInput);
                // do whatever you need to do with this object
            }
            parser.close();
        }catch (JsonParseException e){
            System.out.println(e);
            response = new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }

//        System.out.println(list);
        locationService.createMultipleLocation(carId,list);

        return response;

    }
}
