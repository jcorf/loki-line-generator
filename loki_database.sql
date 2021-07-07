SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP SCHEMA IF EXISTS `loki` ;


CREATE SCHEMA IF NOT EXISTS `loki` DEFAULT CHARACTER SET utf8 ;
USE `loki` ;

DROP TABLE IF EXISTS `loki`.`lines` ;

CREATE TABLE IF NOT EXISTS `loki`.`lines` (
  `line_id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(5000) NOT NULL,
  `type` ENUM("EXPRESSION", "ACTION", "DIALOGUE") NOT NULL,
  PRIMARY KEY (`line_id`))
ENGINE = InnoDB;


DROP TABLE IF EXISTS `loki`.`places` ;

CREATE TABLE IF NOT EXISTS `loki`.`places` (
  `place_id` VARCHAR(100) NOT NULL,
  `place_name` VARCHAR(250) NOT NULL,
  PRIMARY KEY (`place_id`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `loki`.`characters` ;

CREATE TABLE IF NOT EXISTS `loki`.`characters` (
  `character_id` INT NOT NULL AUTO_INCREMENT,
  `character_name` VARCHAR(250) NOT NULL,
  PRIMARY KEY (`character_id`))
ENGINE = InnoDB;


DROP TABLE IF EXISTS `loki`.`scenes` ;

CREATE TABLE IF NOT EXISTS `loki`.`scenes` (
  `scene_id` INT NOT NULL,
  PRIMARY KEY (`scene_id`))
ENGINE = InnoDB;


DROP TABLE IF EXISTS `loki`.`lines_has_scenes` ;

CREATE TABLE IF NOT EXISTS `loki`.`lines_has_scenes` (
  `line_id` INT NOT NULL,
  `scene_id` INT NOT NULL,
  INDEX `fk_lines_has_scenes_line1_idx` (`line_id` ASC) VISIBLE,
  INDEX `fk_lines_is_in_scene_idx` (`scene_id` ASC) VISIBLE,
  CONSTRAINT `fk_lines_has_scenes_line1`
    FOREIGN KEY (`line_id`)
    REFERENCES `loki`.`lines` (`line_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_line_is_in_scene`
    FOREIGN KEY (`scene_id`)
    REFERENCES `loki`.`scenes` (`scene_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


DROP TABLE IF EXISTS `loki`.`lines_has_characters` ;

CREATE TABLE IF NOT EXISTS `loki`.`lines_has_characters` (
  `line_id` INT NOT NULL,
  `character_id` INT NOT NULL,
  INDEX `fk_lines_has_characters_characters1_idx` (`character_id` ASC) VISIBLE,
  INDEX `fk_lines_has_characters_line1_idx` (`line_id` ASC) VISIBLE,
  CONSTRAINT `fk_lines_has_characters_line1`
    FOREIGN KEY (`line_id`)
    REFERENCES `loki`.`lines` (`line_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_lines_has_characters_characters1`
    FOREIGN KEY (`character_id`)
    REFERENCES `loki`.`characters` (`character_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `loki`.`scenes_has_places` ;

CREATE TABLE IF NOT EXISTS `loki`.`scenes_has_places` (
  `scenes_scene_id` INT NOT NULL,
  `places_place_id` VARCHAR(250) NOT NULL,
  INDEX `fk_scenes_has_places_places1_idx` (`places_place_id` ASC) VISIBLE,
  INDEX `fk_scenes_has_places_scenes1_idx` (`scenes_scene_id` ASC) VISIBLE,
  CONSTRAINT `fk_scenes_has_places_scenes1`
    FOREIGN KEY (`scenes_scene_id`)
    REFERENCES `loki`.`scenes` (`scene_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_scenes_has_places_places1`
    FOREIGN KEY (`places_place_id`)
    REFERENCES `loki`.`places` (`place_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


DROP TABLE IF EXISTS `loki`.`switches` ;

CREATE TABLE IF NOT EXISTS `loki`.`switches` (
  `scene_id` INT NOT NULL,
  `old_char_id` INT NOT NULL,
  `new_char_id` INT NOT NULL,
  INDEX `switch_has_scene_idx` (`scene_id` ASC) VISIBLE,
  INDEX `switch_has_old_idx` (`old_char_id` ASC) VISIBLE,
  INDEX `switch_has_new_idx` (`new_char_id` ASC) VISIBLE,
  CONSTRAINT `switch_has_scene`
    FOREIGN KEY (`scene_id`)
    REFERENCES `loki`.`scenes` (`scene_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `switch_has_old`
    FOREIGN KEY (`old_char_id`)
    REFERENCES `loki`.`characters` (`character_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `switch_has_new`
    FOREIGN KEY (`new_char_id`)
    REFERENCES `loki`.`characters` (`character_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

USE loki;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
