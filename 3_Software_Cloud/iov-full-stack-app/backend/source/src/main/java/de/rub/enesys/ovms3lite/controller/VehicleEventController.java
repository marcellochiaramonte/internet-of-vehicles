package de.rub.enesys.ovms3lite.controller;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import de.rub.enesys.ovms3lite.dto.input.VehicleEventInput;
import de.rub.enesys.ovms3lite.dto.output.VehicleEventForList;
import de.rub.enesys.ovms3lite.model.VehicleEvent;
import de.rub.enesys.ovms3lite.repository.VehicleEventRepository;
import de.rub.enesys.ovms3lite.service.VehicleEventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@RestController
public class VehicleEventController extends BaseRestController{

    @Autowired
    private VehicleEventService vehicleEventService;

    @Autowired
    private VehicleEventRepository vehicleEventRepository;

    @PostMapping("event/new")
    VehicleEvent createNewEvent(
            @RequestParam Long timestamp,
            @RequestParam String value,
            @RequestParam String carId,
            @RequestParam Integer metricId
    ){
        System.out.println(timestamp.toString() +" metric: "+ metricId.toString() +" carId: "+carId +" value: "+value);
        return vehicleEventService.createVehicleEvent(timestamp,value,carId,metricId);
    }

    @PostMapping("event/new/multiple")
    ResponseEntity createMultipleEvents(
            @RequestParam String carId,
            @RequestBody  String dataList
    ) throws IOException {
        ObjectMapper mapper = new ObjectMapper();

        List<VehicleEventInput> list = new ArrayList<>();
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
                VehicleEventInput newEvent = new VehicleEventInput();
                newEvent.setT(node.get("t").asLong());
                newEvent.setV(node.get("v").toString());
                newEvent.setId(node.get("id").asInt());
                list.add(newEvent);
                // do whatever you need to do with this object
            }

            parser.close();
        }catch (JsonParseException e){
            System.out.println(e);
            response = new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }

        vehicleEventService.createMultipleVehicleEvents(carId,list);

        return response;

    }


    @GetMapping("events/filter")
    List<VehicleEventForList> findAllVehicles(
            @RequestParam String vehicleUuid,
            @RequestParam Integer metricId,
            @RequestParam Long startTimestamp,
            @RequestParam Long endTimestamp
    ){
        return vehicleEventService.getEventsFilterByTimeAndMetric(vehicleUuid,metricId,startTimestamp,endTimestamp);

    }

    @GetMapping("events/all")
    List<VehicleEventForList> findAllVehicles(){
        return vehicleEventService.getAll();

    }

}
