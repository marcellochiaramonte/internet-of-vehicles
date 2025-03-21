package de.rub.enesys.ovms3lite.service;

import de.rub.enesys.ovms3lite.dto.output.VehicleForListOutput;
import de.rub.enesys.ovms3lite.mapper.VehicleMapper;
import de.rub.enesys.ovms3lite.model.Vehicle;
import de.rub.enesys.ovms3lite.repository.VehicleRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@Transactional
public class VehicleService {

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private VehicleMapper vehicleMapper;

    public VehicleForListOutput findOneByUuid(String uuid){
        Optional<Vehicle> found = vehicleRepository.findOneById(uuid);
        if(found.isPresent()){
            return vehicleMapper.vehicleOutputForVehicleList(found.get());
        }
        else{
            return null;
        }
    }

    public Optional<Vehicle> findOneById(String carId){
        return vehicleRepository.findOneById(carId);
    }


    public List<Vehicle> findAllByOrderByName(){
        return vehicleRepository.findAllByOrderByModel();
    }
}
