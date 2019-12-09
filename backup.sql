
--Database: quiz

CREATE TABLE `ADSToken` (
  `ADSTokenID` int(11) NOT NULL AUTO_INCREMENT,
  `Network` text,
  `Title` text,
  `Value` text,
  PRIMARY KEY (`ADSTokenID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


CREATE TABLE `Account` (
  `AccountID` int(11) NOT NULL,
  `AccountNumber` int(11) NOT NULL,
  `AccountName` int(11) NOT NULL,
  `Bank` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  PRIMARY KEY (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Admin` (
  `AdminID` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` text COLLATE utf8mb4_unicode_ci,
  `PassHash` text COLLATE utf8mb4_unicode_ci,
  `Estate` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`AdminID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Choice` (
  `ChoiceID` int(11) NOT NULL AUTO_INCREMENT,
  `QuestionID` int(11) NOT NULL,
  `Title` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IsTrue` char(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ChoiceID`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Contest` (
  `ContestID` int(11) NOT NULL,
  `StartTime` int(11) NOT NULL,
  `EndTime` int(11) NOT NULL,
  `NewAttribute` int(11) NOT NULL,
  PRIMARY KEY (`ContestID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Invoice` (
  `InvoiceID` int(11) NOT NULL,
  `Estate` int(11) NOT NULL,
  `PackageID` int(11) NOT NULL,
  PRIMARY KEY (`InvoiceID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `LogID` (
  `LogID` int(11) NOT NULL,
  `Action` int(11) NOT NULL,
  `SessionID` int(11) NOT NULL,
  `Time` int(11) NOT NULL,
  `SessionToken` int(11) NOT NULL,
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `LotteryItem` (
  `LotteryItemID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Estate` mediumtext COLLATE utf8mb4_unicode_ci,
  `Type` mediumtext COLLATE utf8mb4_unicode_ci,
  `Amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`LotteryItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `MoneyRequest` (
  `MoneyRequestID` int(11) NOT NULL AUTO_INCREMENT,
  `Estate` text COLLATE utf8mb4_unicode_ci,
  `BankAccount` text COLLATE utf8mb4_unicode_ci,
  `AccountName` text COLLATE utf8mb4_unicode_ci,
  `Amount` bigint(20) DEFAULT NULL,
  `RequestDate` text COLLATE utf8mb4_unicode_ci,
  `UserName` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`MoneyRequestID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `OptionParameter` (
  `OptionParameterID` int(11) NOT NULL AUTO_INCREMENT,
  `Tag` text COLLATE utf8mb4_unicode_ci,
  `Title` text COLLATE utf8mb4_unicode_ci,
  `Value` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`OptionParameterID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `Package` (
  `PackageID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text COLLATE utf8mb4_unicode_ci,
  `Price` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL,
  PRIMARY KEY (`PackageID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `Question` (
  `OrderNum` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL AUTO_INCREMENT,
  `QuestionType` char(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `QuestionStatement` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PackageID` int(11) DEFAULT NULL,
  `ContestID` int(11) DEFAULT NULL,
  `Prize` char(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IsSaftyLevel` char(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `AnswerTime` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`QuestionID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `Session` (
  `SessionID` int(11) NOT NULL AUTO_INCREMENT,
  `Token` char(255) NOT NULL,
  `UserID` char(255) NOT NULL,
  `Estate` char(255) NOT NULL,
  PRIMARY KEY (`SessionID`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=latin1;


CREATE TABLE `User` (
  `DisplayName` text,
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `Score` int(11) DEFAULT NULL,
  `WeeklyScore` int(11) DEFAULT NULL,
  `AllowedPackageCount` int(11) DEFAULT NULL,
  `UserName` char(255) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `PasswordHash` char(255) DEFAULT NULL,
  `PhoneNumber` text,
  `Rank` int(11) DEFAULT NULL,
  `WeeklyRank` int(11) DEFAULT NULL,
  `ReferralCode` text,
  `Balance` int(11) DEFAULT NULL,
  `TotalTrueAnswers` int(11) DEFAULT NULL,
  `TotalFalseAnswers` int(11) DEFAULT NULL,
  `TotalPaid` int(11) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserName` (`UserName`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;


CREATE TABLE `Video` (
  `VideoID` int(11) NOT NULL AUTO_INCREMENT,
  `Address` text COLLATE utf8mb4_unicode_ci,
  `Title` text COLLATE utf8mb4_unicode_ci,
  `Reserve2` blob,
  PRIMARY KEY (`VideoID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `WeeklyRecord` (
  `WeeklyRecordID` int(11) NOT NULL AUTO_INCREMENT,
  `WeekEndData` text COLLATE utf8mb4_unicode_ci,
  `Score` int(11) DEFAULT NULL,
  `UserName` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`WeeklyRecordID`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
