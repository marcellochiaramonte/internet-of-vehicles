package de.rub.enesys.ovms3lite.controller;

import de.rub.enesys.ovms3lite.dto.output.VehicleForListOutput;
import de.rub.enesys.ovms3lite.mapper.VehicleMapper;
import de.rub.enesys.ovms3lite.model.Vehicle;
import de.rub.enesys.ovms3lite.repository.VehicleRepository;
import de.rub.enesys.ovms3lite.service.VehicleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
public class VehicleController extends BaseRestController{

    @Autowired
    private VehicleService vehicleService;

    @Autowired
    private VehicleMapper vehicleMapper;

    @GetMapping("vehicles/find")
    VehicleForListOutput findFullVehicle(@RequestParam String id){
        return vehicleService.findOneByUuid(id);
    }

    @GetMapping("vehicles/all")
    List<VehicleForListOutput> findAllVehicles(){
        return vehicleMapper.vehicleOutputListForVehicleList(vehicleService.findAllByOrderByName());
    }
}
