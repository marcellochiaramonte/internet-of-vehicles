package de.rub.enesys.ovms3lite.repository;

import de.rub.enesys.ovms3lite.model.Vehicle;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VehicleRepository extends CrudRepository<Vehicle,Long> {

    Optional<Vehicle> findOneById(String id);

    List<Vehicle> findAllByOrderByModel();

}
